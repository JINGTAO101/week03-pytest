import pytest

@pytest.mark.skip(reason="演示：这条先不跑")
def test_marks_skip():
    assert False

@pytest.mark.xfail(reason="演示：这条会失败，但不算测试失败")
def test_marks_xfail():
    assert 1==2
