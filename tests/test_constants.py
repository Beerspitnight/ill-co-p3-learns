# tests/test_constants.py
import pytest
from learning_app.scripts.constants import get_all_options, Icons

def test_get_all_options():
    opts = get_all_options()
    assert 'ELEMENT' in opts and isinstance(opts['ELEMENT'], list)
    assert 'PRINCIPLE' in opts and isinstance(opts['PRINCIPLE'], list)

def test_icons_enum():
    assert hasattr(Icons, 'BACK')
    assert Icons.BACK.value.endswith('.svg')
    assert Icons.NEXT.value == 'next.svg'
