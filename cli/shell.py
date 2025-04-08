import cmd
import sys
from utils import logger, get_file_path_from_output, fetch_topic_data, generate_podcast_script, generate_audio_file

class Whisper(cmd.Cmd):
    intro = "Welcome to WhisperCast! Type 'help' to list commands."
    prompt = "(whisper) "

    def __init__(self, completekey = "tab", stdin = None, stdout = None):
        super().__init__(completekey, stdin, stdout)

    def do_topic(self, arg: str) -> None:
        logger.info(f"Finding content for '{arg}'")
        content = fetch_topic_data(arg)
        logger.success(f"Fetched content")
        content = generate_podcast_script(arg, content, 5)
        generate_audio_file(content, arg.capitalize())


    def do_rss(self, arg: str) -> None:
        logger.info(f"Generating podcast for '{arg}'")

    @logger.catch
    def do_play(self, arg: str) -> None:
        try:
            if(get_file_path_from_output(arg)):
                logger.info(f"Playing: {arg}")
            else:
                logger.error(f"{arg} file not found in output folder!")
        except Exception as e:
            logger.critical(e)

    def do_bye(self, arg: str) -> None:
        logger.info("Shutting down whisper..\nDone")
        sys.exit(0)
