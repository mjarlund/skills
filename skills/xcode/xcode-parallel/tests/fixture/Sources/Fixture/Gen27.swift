public func gen27(_ x: Int) -> Int { (1...50).map { $0 * x }.reduce(0, +) + 27 }
