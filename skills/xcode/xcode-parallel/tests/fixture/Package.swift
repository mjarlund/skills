// swift-tools-version:5.9
import PackageDescription
let package = Package(
  name: "Fixture",
  platforms: [.iOS(.v16), .macOS(.v13)],
  products: [.library(name: "Fixture", targets: ["Fixture"])],
  targets: [
    .target(name: "Fixture"),
    .testTarget(name: "FixtureTests", dependencies: ["Fixture"]),
  ])
