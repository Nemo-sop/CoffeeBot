from backend.app.services.validators.language import is_spanish

def test_detects_spanish():
    assert is_spanish("¿Cómo se hace un café?") is True

def test_detects_non_spanish():
    assert is_spanish("How do you make coffee?") is False
