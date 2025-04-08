from cli import Whisper
from utils import logger
import sys


if __name__ == "__main__":
    try:
        Whisper().cmdloop()
    except KeyboardInterrupt:
        logger.info("Keyboard Interrupt! Shutting down Whisper...\nDone")
        sys.exit(0)
    except Exception as e:
        logger.error(e)