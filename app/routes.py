from fastapi import APIRouter, Depends, Header
import uuid
import producers
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_LOG_FILE = BASE_DIR / 'app.log'


def setup_logger(log_file=DEFAULT_LOG_FILE):
    file_log = logging.FileHandler(log_file)
    console_out = logging.StreamHandler()

    logging.basicConfig(
        handlers=(file_log, console_out),
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    return logger


logger = setup_logger()


def write_log(message):
    logger.info(message)


router = APIRouter()


def check_x_flag(x_flag: str = Header(None)):
    return x_flag


@router.get("/generate-uuid")
async def generate_uuid(x_flag: str = Depends(check_x_flag)):
    generated_uuid = str(uuid.uuid4())
    if x_flag == "green":
        write_log(f"{generated_uuid} GREEN")
    elif x_flag == "red":
        producers.enqueue_message(f"{generated_uuid} RED")
    return {"uuid": generated_uuid}
