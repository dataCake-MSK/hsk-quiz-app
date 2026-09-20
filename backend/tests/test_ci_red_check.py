def test_ci_should_fail_on_purpose():
    """CI가 실패를 실제로 빨강으로 표시하는지 확인하는 임시 테스트 (확인 후 되돌림)."""
    assert 1 == 2
