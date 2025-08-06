from backend.app.services.validators.topic import is_related_to_coffee

def test_related_to_coffee():
    assert is_related_to_coffee("El espresso es una forma concentrada de café.") is True

def test_not_related_to_coffee():
    assert is_related_to_coffee("Me gustan los gatos y los perros.") is False
