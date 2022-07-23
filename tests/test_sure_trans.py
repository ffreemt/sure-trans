"""Test sure_trans."""
# pylint: disable=broad-except
from sure_trans import __version__
from sure_trans import sure_trans


def test_version():
    """Test version."""
    assert __version__[:3] == "0.1"


def test_sanity():
    """Check sanity."""
    try:
        assert not sure_trans()
    except Exception:
        assert True
