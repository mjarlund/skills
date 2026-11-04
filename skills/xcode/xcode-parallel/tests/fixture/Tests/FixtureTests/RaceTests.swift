import XCTest
@testable import Fixture
// Writes a per-worktree value into simulator-wide state, waits, reads it back.
// On a simulator shared with another worktree's run, the value gets overwritten.
final class RaceTests: XCTestCase {
  func testSimulatorStateIsPrivate() {
    let d = UserDefaults(suiteName: "xc-parallel-selftest")!
    d.set(owner, forKey: "owner"); d.synchronize()
    Thread.sleep(forTimeInterval: 8)
    d.synchronize()
    XCTAssertEqual(d.string(forKey: "owner"), owner)
  }
  func testMath() { XCTAssertEqual(gen1(1), 1276) }
}
