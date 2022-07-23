"""Test sure_trans."""
# pylint: disable=broad-except
from sure_trans import __version__, sure_trans


def test_version():
    """Test version."""
    assert __version__[:3] == "0.1"


def test_sanity():
    """Check sanity."""
    try:
        assert not sure_trans()
    except Exception:
        assert True


def test_sure_trans1():
    """Test 1."""
    res = sure_trans("书山有路勤为径", to_language="en")

    assert len(res) > 10
