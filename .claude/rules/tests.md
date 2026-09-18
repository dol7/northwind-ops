---
paths:
  - "**/test_*.py"
---

# Test files

Loaded only when Claude reads a test file. Tests sit next to the code they test in every
package, so this one glob gives all of them the same convention.

- Plain `assert` with pytest. No `unittest.TestCase`, and no mocks of our own code.
- Name tests for behaviour: `test_<what>_<outcome>`.
- Give every test body three marker comments, in order: `# arrange`, `# act`, `# assert`.
- No network, no real clock (pass `today` / `now` in), no randomness.
- Build money in tests with `Decimal("...")` from a string, never a float.
- New behaviour gets a test in the sibling `test_<module>.py`. Never create a `tests/` directory.
