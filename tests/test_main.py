import pytest
from unittest import mock

from typer.testing import CliRunner

from mailograf.main import app


@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_db():
    with mock.patch("mailograf.main.db", autospec=True) as db:
        yield db

def test_tags(runner: CliRunner, mock_db: mock.Mock):
    fake_tags = mock.MagicMock(return_value = [])

    result = runner.invoke(app, ["tags"])
    assert result.exit_code == 0
    assert "showing tags" in result.stdout

    mock_db.get_all_tags.assert_called_once()
