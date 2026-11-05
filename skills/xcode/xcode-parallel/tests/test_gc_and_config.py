#!/usr/bin/env python3
"""Fast, no-Xcode unit tests for the gc() safety rules and the build/test target split in `xc`.
Run: python3 -I tests/test_gc_and_config.py
Loads scripts/xc as a module (it has no .py extension) and monkeypatches CACHE/simctl/run so
nothing here touches the machine's real simulators or ~/Library/Caches/xc-parallel.
"""
import json
import os
import shutil
import sys
import tempfile
import time
import types
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
XC_PATH = os.path.join(HERE, "..", "scripts", "xc")


def load_xc():
    src = open(XC_PATH).read()
    mod = types.ModuleType("xc_under_test")
    exec(compile(src, XC_PATH, "exec"), mod.__dict__)
    return mod


xc = load_xc()


def make_state_dir(cache, name, path, sims=None, last_used=None, cfg=None):
    sd = os.path.join(cache, name)
    os.makedirs(sd, exist_ok=True)
    meta = {"path": path, "sims": sims or {}, "last_used": last_used if last_used is not None else time.time()}
    with open(os.path.join(sd, "meta.json"), "w") as f:
        json.dump(meta, f)
    with open(os.path.join(sd, "config.json"), "w") as f:
        json.dump(cfg or {}, f)
    return sd


class GcSafetyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.cache = os.path.join(self.tmp, "cache")
        os.makedirs(os.path.join(self.cache, "slots"))
        self._orig_cache = xc.CACHE
        xc.CACHE = self.cache
        self.deleted_sims = []
        self._orig_delete_sim = xc.delete_sim
        xc.delete_sim = lambda udid: self.deleted_sims.append(udid)
        self._orig_simctl_json = xc.simctl_json
        xc.simctl_json = lambda what: {"devices": {}} if what == "devices" else {}
        self._orig_run = xc.run
        shutdowns = self.shutdowns = []
        def fake_run(cmd, **kw):
            if cmd[:3] == ["xcrun", "simctl", "shutdown"]:
                shutdowns.append(cmd[3])
            class R:
                returncode = 0
                stdout = ""
                stderr = ""
            return R()
        xc.run = fake_run
        self._orig_enforce = xc.enforce_budget
        xc.enforce_budget = lambda **kw: None

    def tearDown(self):
        xc.CACHE = self._orig_cache
        xc.delete_sim = self._orig_delete_sim
        xc.simctl_json = self._orig_simctl_json
        xc.run = self._orig_run
        xc.enforce_budget = self._orig_enforce
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_dry_run_changes_nothing(self):
        sd = make_state_dir(self.cache, "gone1", "/no/such/worktree", sims={"ios": {"udid": "AAA", "name": "xcp-gone1-ios"}})
        xc.gc(verbose=False, dry_run=True)
        self.assertTrue(os.path.isdir(sd), "dry run must not delete the state dir")
        self.assertEqual(self.deleted_sims, [], "dry run must not delete any simulator")

    def test_removed_worktree_is_reclaimed(self):
        sd = make_state_dir(self.cache, "gone2", "/no/such/worktree", sims={"ios": {"udid": "BBB", "name": "xcp-gone2-ios"}})
        xc.gc(verbose=False, dry_run=False)
        self.assertFalse(os.path.isdir(sd), "state of a removed worktree should be reclaimed")
        self.assertIn("BBB", self.deleted_sims)

    def test_active_lock_protects_removed_worktree_state(self):
        """Even if the worktree dir is gone, a held worktree.lock (something still mid-run) must
        stop gc from touching that state dir or its simulator."""
        sd = make_state_dir(self.cache, "gone3", "/no/such/worktree", sims={"ios": {"udid": "CCC", "name": "xcp-gone3-ios"}})
        held = xc.Lock(os.path.join(sd, "worktree.lock"), "fake active run")
        self.assertTrue(held.try_acquire())
        try:
            xc.gc(verbose=False, dry_run=False)
            self.assertTrue(os.path.isdir(sd), "must not delete state dir whose lock is held")
            self.assertNotIn("CCC", self.deleted_sims)
        finally:
            held.release()

    def test_idle_live_worktree_sim_is_shut_down_not_deleted(self):
        live = os.path.join(self.tmp, "live-worktree")
        os.makedirs(live)
        xc.simctl_json = lambda what: {"devices": {"iOS 18": [{"udid": "DDD", "name": "xcp-live-ios", "state": "Booted", "isAvailable": True}]}} if what == "devices" else {}
        make_state_dir(self.cache, "live1", live, sims={"ios": {"udid": "DDD", "name": "xcp-live-ios"}}, last_used=time.time() - 3600)
        xc.gc(verbose=False, idle_min=45, dry_run=False)
        self.assertIn("DDD", self.shutdowns, "idle simulator of a live worktree should be shut down")
        self.assertEqual(self.deleted_sims, [], "a live worktree's simulator must not be deleted, only shut down")

    def test_busy_live_worktree_is_left_alone(self):
        live = os.path.join(self.tmp, "live-worktree2")
        os.makedirs(live)
        sd = make_state_dir(self.cache, "live2", live, sims={"ios": {"udid": "EEE", "name": "xcp-live2-ios"}}, last_used=time.time() - 3600)
        held = xc.Lock(os.path.join(sd, "worktree.lock"), "another xc command")
        self.assertTrue(held.try_acquire())
        try:
            xc.gc(verbose=False, idle_min=45, dry_run=False)
            self.assertEqual(self.shutdowns, [])
            self.assertEqual(self.deleted_sims, [])
        finally:
            held.release()

    def test_template_simulator_never_touched_by_orphan_reap(self):
        xc.simctl_json = lambda what: {"devices": {"iOS 18": [
            {"udid": "TEMPLATE", "name": "xcp-template-abc123", "state": "Shutdown", "isAvailable": True},
            {"udid": "UNRELATED", "name": "some-other-sim", "state": "Shutdown", "isAvailable": True},
        ]}} if what == "devices" else {}
        xc.gc(verbose=False, dry_run=False)
        self.assertEqual(self.deleted_sims, [], "a template or non-xcp simulator must never be reaped as an orphan")

    def test_orphan_xcp_sim_with_no_known_worktree_is_reaped(self):
        xc.simctl_json = lambda what: {"devices": {"iOS 18": [
            {"udid": "ORPHAN", "name": "xcp-forgotten-worktree-ios", "state": "Shutdown", "isAvailable": True},
        ]}} if what == "devices" else {}
        xc.gc(verbose=False, dry_run=False)
        self.assertIn("ORPHAN", self.deleted_sims)


class TargetSplitTests(unittest.TestCase):
    def test_tkey_namespaces_project_and_scheme_only(self):
        self.assertEqual(xc.tkey("project", "build"), "project:build")
        self.assertEqual(xc.tkey("scheme", "test"), "scheme:test")
        self.assertEqual(xc.tkey("platform", "test"), "platform")  # shared, not namespaced

    def test_target_for_command(self):
        self.assertEqual(xc.target_for("test"), "test")
        for cmd in ("build", "run", "sim", "env"):
            self.assertEqual(xc.target_for(cmd), "build")

    def test_explicit_project_flag_is_reported_as_one_off(self):
        class FakeState:
            cfg = {}
        p, explicit = xc.find_project(FakeState(), __file__, "test")
        self.assertTrue(explicit, "a --project flag must be reported as explicit/one-off")
        self.assertEqual(p, os.path.abspath(__file__))

    def test_cached_project_for_one_target_does_not_leak_into_the_other(self):
        empty_dir = tempfile.mkdtemp()
        try:
            class FakeState:
                cfg = {"project:build": __file__}
                root = empty_dir
            # Resolving the TEST target must not see the BUILD target's cached project; with
            # nothing discoverable under root, find_project must fail rather than fall back to it.
            with self.assertRaises(SystemExit):
                xc.find_project(FakeState(), None, "test")
        finally:
            shutil.rmtree(empty_dir, ignore_errors=True)

    def test_remember_skips_explicit_choices(self):
        class FakeState:
            def __init__(self):
                self.cfg = {}
                self.saved = False
            def save(self):
                self.saved = True
        st = FakeState()
        xc.remember(st, "build", "/some/proj.xcodeproj", True, "SomeScheme", True)
        self.assertNotIn("project:build", st.cfg, "an explicit one-off --project must never be remembered")
        self.assertNotIn("scheme:build", st.cfg)
        self.assertFalse(st.saved)

    def test_remember_persists_auto_detected_choices(self):
        class FakeState:
            def __init__(self):
                self.cfg = {}
                self.saved = False
            def save(self):
                self.saved = True
        st = FakeState()
        xc.remember(st, "test", "/pkg/Package.swift", False, "Pkg-Package", False)
        self.assertEqual(st.cfg["project:test"], "/pkg/Package.swift")
        self.assertEqual(st.cfg["scheme:test"], "Pkg-Package")
        self.assertTrue(st.saved)


if __name__ == "__main__":
    unittest.main()
