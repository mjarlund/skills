---
type: llm
focus: trace
weight: 1
---

The agent ran `xc test` against the package's own scheme/project (packages/Package.swift,
"MyApp-Package"), not the app's remembered build default ("MyApp Debug" / app/MyApp.xcodeproj),
either by passing --project/--scheme for that call or by setting the test target default with
`xc config set --target test ...`.
