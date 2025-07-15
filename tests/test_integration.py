import sys
import pytest
from io import StringIO
from unittest.mock import patch


def test_cli_filter(capsys, monkeypatch):
    monkeypatch.setattr(sys, 'argv', [
        'main.py',
        '--file', 'tests/test_data/sample.csv',
        '--where', 'price>150'
    ])

    from main import main
    main()

    captured = capsys.readouterr()
    assert "B" in captured.out


def test_cli_aggregate(capsys, monkeypatch):
    monkeypatch.setattr(sys, 'argv', [
        'main.py',
        '--file', 'tests/test_data/sample.csv',
        '--aggregate', 'price=avg'
    ])

    from main import main
    main()

    captured = capsys.readouterr()
    assert "200.00" in captured.out
