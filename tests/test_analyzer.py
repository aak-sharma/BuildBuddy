from app.analyzer import analyze_log, summarize


def test_detects_missing_dependency():
    findings = analyze_log("ModuleNotFoundError: No module named 'requests'")
    assert findings[0].category == "Dependency"
    assert findings[0].title == "Missing Python package"


def test_detects_test_failure():
    findings = analyze_log("FAILED tests/test_app.py::test_home - AssertionError")
    assert any(f.category == "Testing" for f in findings)


def test_unknown_log_returns_fallback():
    findings = analyze_log("Build started successfully. Waiting...")
    assert len(findings) == 1
    assert findings[0].category == "Unclassified"


def test_summary_counts_severity():
    findings = analyze_log("SyntaxError: invalid syntax")
    result = summarize(findings)
    assert result["total_findings"] == 1
    assert result["severity_counts"]["High"] == 1
