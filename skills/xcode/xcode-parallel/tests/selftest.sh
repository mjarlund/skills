#!/usr/bin/env bash
# Proves the isolation claim on YOUR machine: N git worktrees run the same simulator test at once.
#   tests/selftest.sh            # through xc          -> expect all PASS
#   tests/selftest.sh --naive    # shared simulator   -> expect failures (the problem xc solves)
# Usage: selftest.sh [--naive] [N]   (N worktrees, default 3). Needs Xcode; ~3-6 min first time.
set -u
MODE=xc; N=3
for a in "$@"; do case $a in --naive) MODE=naive;; [0-9]*) N=$a;; esac; done
HERE=$(cd "$(dirname "$0")" && pwd)
XC="$HERE/../scripts/xc"
T=$(mktemp -d /tmp/xc-selftest.XXXXXX)
cleanup() { (cd "$T/main" 2>/dev/null && for i in $(seq 1 "$N"); do git worktree remove --force "../wt$i" 2>/dev/null; done); python3 "$XC" gc >/dev/null 2>&1; [ -n "${NAIVE_SIM:-}" ] && { xcrun simctl shutdown "$NAIVE_SIM"; xcrun simctl delete "$NAIVE_SIM"; } >/dev/null 2>&1; rm -rf "$T"; }
trap cleanup EXIT
mkdir -p "$T/main" && cp -R "$HERE/fixture/." "$T/main/" && cd "$T/main" || exit 1
git init -q -b main . && git add -A && git -c user.email=t@t -c user.name=t commit -qm init
for i in $(seq 1 "$N"); do
  git worktree add -q "../wt$i" -b "wt$i"
  echo "public let owner = \"wt$i\"" > "../wt$i/Sources/Fixture/Owner.swift"
done
echo "mode=$MODE worktrees=$N dir=$T"
if [ "$MODE" = naive ]; then
  read -r RT DT < <(xcrun simctl list -j runtimes | /usr/bin/python3 -c "
import json,re,sys
r=[x for x in json.load(sys.stdin)['runtimes'] if x['platform']=='iOS' and x['isAvailable']]
r=max(r,key=lambda x:[int(i) for i in x['version'].split('.')])
p=[t for t in r['supportedDeviceTypes'] if re.fullmatch(r'iPhone \\d+',t['name'])]
p.sort(key=lambda t:int(t['name'].split()[1]))
print(r['identifier'],(p or r['supportedDeviceTypes'])[-1]['identifier'])")
  NAIVE_SIM=$(xcrun simctl create xcp-selftest-shared "$DT" "$RT"); xcrun simctl bootstatus "$NAIVE_SIM" -b >/dev/null
fi
for i in $(seq 1 "$N"); do
  ( cd "../wt$i"
    if [ "$MODE" = naive ]; then xcodebuild test -scheme Fixture -destination "id=$NAIVE_SIM" -parallel-testing-enabled NO >"$T/wt$i.log" 2>&1
    else python3 "$XC" test >"$T/wt$i.log" 2>&1; fi
    echo $? >"$T/wt$i.rc" ) &
done
wait
pass=0
for i in $(seq 1 "$N"); do
  if [ "$(cat "$T/wt$i.rc")" = 0 ]; then echo "wt$i PASS"; pass=$((pass+1)); else echo "wt$i FAIL"; grep -hE "FAIL |error:|XCTAssert" "$T/wt$i.log" | head -3 | sed 's/^/    /'; fi
done
echo "$pass/$N passed ($MODE)"
[ "$MODE" = naive ] && exit 0
[ "$pass" = "$N" ]
