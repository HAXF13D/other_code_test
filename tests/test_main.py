import os
import pytest
from fastapi.testclient import TestClient
from app import main
from pathlib import Path
import io
import logging
import time

BASE_DIR = Path(__file__).resolve().parent.parent
client = TestClient(main.app)


def clear_log_file():
    log_file_path = f"{BASE_DIR}/app.log"
    if os.path.exists(log_file_path):
        with open(log_file_path, 'w'):
            pass


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    clear_log_file()
    yield
    clear_log_file()


def test_generate_uuid():
    response = client.get("/generate-uuid")
    assert response.status_code == 200
    assert "uuid" in response.json()
    assert isinstance(response.json()["uuid"], str)


def test_green_flag():
    console_capture = io.StringIO()
    console_out = logging.StreamHandler(console_capture)

    root_logger = logging.getLogger()
    root_logger.addHandler(console_out)
    root_logger.setLevel(logging.INFO)

    headers = {
        'Content-Type': 'application/json',
        'x-flag': 'green',
    }
    response = client.get("/generate-uuid", headers=headers)
    assert response.status_code == 200
    assert "uuid" in response.json()
    assert isinstance(response.json()["uuid"], str)

    expected_log_message = f"{response.json()['uuid']} GREEN"
    console_capture.seek(0)
    captured_output = console_capture.getvalue()
    assert expected_log_message in captured_output

    root_logger.removeHandler(console_out)


def test_red_flag():
    headers = {
        'Content-Type': 'application/json',
        'x-flag': 'red',
    }
    response = client.get("/generate-uuid", headers=headers)
    assert response.status_code == 200
    assert "uuid" in response.json()
    assert isinstance(response.json()["uuid"], str)

    expected_log_message = f"{response.json()['uuid']} RED"

    time.sleep(1)

    with open(f"{BASE_DIR}/app.log", 'r') as file:
        logs = file.readlines()
        assert any(expected_log_message in log for log in logs)
