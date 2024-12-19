import csv
import os
from tempfile import NamedTemporaryFile
from unittest.mock import patch

import pytest

from src.python_src.util.lookup_table import get_max_ratings_by_code


def create_temp_csv(content: list[list[str]]) -> str:
    temp_file = NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    writer = csv.writer(temp_file)
    for row in content:
        writer.writerow(row)
    temp_file.close()
    return temp_file.name


def test_get_max_ratings_by_code_with_invalid_csv_line() -> None:
    content = [
        [
            'Diagnostic Code',
            'Rated Issue Name',
            'Max Rating',
            'Body System',
            'Category',
            'Subcategory',
        ],  # Missing CFR Reference
        ['6260', 'Tinnitus', '10', 'Ear', 'Diseases', 'Inner Ear'],
    ]
    temp_file = create_temp_csv(content)

    try:
        with patch('src.python_src.util.lookup_table.os.path.join', return_value=temp_file):
            with pytest.raises(ValueError, match='Invalid CSV line at index 1'):
                get_max_ratings_by_code()
    finally:
        os.unlink(temp_file)


def test_get_max_ratings_by_code_with_invalid_diagnostic_code() -> None:
    content = [
        ['Diagnostic Code', 'Rated Issue Name', 'Max Rating', 'Body System', 'Category', 'Subcategory', 'CFR Reference'],
        ['invalid', 'Tinnitus', '10', 'Ear', 'Diseases', 'Inner Ear', '4.87'],
    ]
    temp_file = create_temp_csv(content)

    try:
        with patch('src.python_src.util.lookup_table.os.path.join', return_value=temp_file):
            with pytest.raises(ValueError, match='Invalid diagnostic code or max rating at index 1'):
                get_max_ratings_by_code()
    finally:
        os.unlink(temp_file)


def test_get_max_ratings_by_code_with_invalid_max_rating() -> None:
    content = [
        ['Diagnostic Code', 'Rated Issue Name', 'Max Rating', 'Body System', 'Category', 'Subcategory', 'CFR Reference'],
        ['6260', 'Tinnitus', 'invalid', 'Ear', 'Diseases', 'Inner Ear', '4.87'],
    ]
    temp_file = create_temp_csv(content)

    try:
        with patch('src.python_src.util.lookup_table.os.path.join', return_value=temp_file):
            with pytest.raises(ValueError, match='Invalid diagnostic code or max rating at index 1'):
                get_max_ratings_by_code()
    finally:
        os.unlink(temp_file)


def test_get_max_ratings_by_code_with_missing_max_rating() -> None:
    content = [
        ['Diagnostic Code', 'Rated Issue Name', 'Max Rating', 'Body System', 'Category', 'Subcategory', 'CFR Reference'],
        ['6260', 'Tinnitus', '', 'Ear', 'Diseases', 'Inner Ear', '4.87'],
    ]
    temp_file = create_temp_csv(content)

    try:
        with patch('src.python_src.util.lookup_table.os.path.join', return_value=temp_file):
            result = get_max_ratings_by_code()
            assert result == {}
    finally:
        os.unlink(temp_file)
