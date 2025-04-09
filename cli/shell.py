import os
import cmd
import sys
import glob
import subprocess
from utils import logger, get_file_path_from_output, fetch_topic_data, generate_podcast_script, generate_audio_file, generate_audiobook, extract_content


class Whisper(cmd.Cmd):
    os.system('clear')
    intro = "Welcome to WhisperCast! Type 'help' to list commands."
    prompt = "(whisper) "

    def __init__(self, completekey = "tab", stdin = None, stdout = None):
        super().__init__(completekey, stdin, stdout)

    def do_podcast(self, arg: str) -> None:
        logger.info(f"Podcast generation started")
        content = fetch_topic_data(arg)
        content = generate_podcast_script(arg, content, 5)
        generate_audio_file(content, arg.capitalize())

    def do_audiobook(self, arg: str) -> None:
        logger.info(f"Generating audiobook for '{arg}'")
        content = extract_content(arg)
        content = generate_audiobook(content)
        generate_audio_file(content, "User_Audiobook")

    def do_sensei(self, arg: str) -> None:
        logger.info(f"Entering sensei mode")

    def do_clear(self, args: str) -> None:
        os.system('clear')

    def do_ls(self, args: str) -> None:
        """
        List all available audio files in the output directory.
        """
        output_dir = "output"
        if not os.path.exists(output_dir):
            logger.warning("Output directory does not exist.")
            return

        audio_files = glob.glob(os.path.join(output_dir, "*.wav"))
        if not audio_files:
            logger.info("No audio files found in the output directory.")
            return

        print("\nAvailable audio files:")
        for idx, file in enumerate(audio_files, start=1):
            print(f"{idx}. {os.path.basename(file)}")

    @logger.catch
    def do_play(self, arg: str) -> None:
        """
        Play an audio file by selecting its number from the ls command.
        """
        try:
            output_dir = "output"
            audio_files = glob.glob(os.path.join(output_dir, "*.wav"))
            if not audio_files:
                logger.error("No audio files available to play.")
                print("No audio files available. Use 'ls' to check.")
                return

            try:
                file_index = int(arg) - 1
                if file_index < 0 or file_index >= len(audio_files):
                    logger.error("Invalid file number selected.")
                    logger.info("Invalid file number. Use 'ls' to list available files.")
                    return

                file_to_play = audio_files[file_index]
                logger.info(f"Playing: {file_to_play}")
                logger.info(f"Playing: {os.path.basename(file_to_play)}")
                subprocess.run(["afplay", file_to_play])
            except ValueError:
                logger.error("Invalid input. Please provide a valid file number.")
        except Exception as e:
            logger.critical(f"Error while playing audio: {e}")

    def do_bye(self, arg: str) -> None:
        logger.info("Shutting down whisper..\nDone")
        sys.exit(0)
