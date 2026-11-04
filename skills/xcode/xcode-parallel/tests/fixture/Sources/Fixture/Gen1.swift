public func gen1(_ x: Int) -> Int { (1...50).map { $0 * x }.reduce(0, +) + 1 }
