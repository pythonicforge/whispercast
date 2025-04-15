from cli import Whisper
from utils import logger
from utils.env_checker import check_env_file_exists
import sys


if __name__ == "__main__":
    try:
        check_env_file_exists()
        Whisper().cmdloop()
    except KeyboardInterrupt:
        logger.info("Keyboard Interrupt! Shutting down Whisper...\nDone")
        sys.exit(0)
    except Exception as e:
        logger.error(e)