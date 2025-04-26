import pytest
from learning_app.utils.data_loader import load_dataset, get_shuffled_dataset, get_image_by_filename

def test_load_dataset():
    data = load_dataset()
    assert isinstance(data, list)
    assert len(data) > 0

def test_shuffled_dataset():
    data = get_shuffled_dataset()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_image_by_filename():
    data = load_dataset()
    first = data[0]
    filename = first.get('image_filename')
    result = get_image_by_filename(filename)
    assert isinstance(result, dict)
    assert result.get('image_filename') == filename
    assert get_image_by_filename('nonexistent.png') is None
