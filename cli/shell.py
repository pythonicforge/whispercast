import os
import cmd
import sys
import glob
import subprocess
from utils import logger, get_file_path_from_output, fetch_topic_data, generate_podcast_script, generate_audio_file, generate_audiobook, extract_content
from groq import Groq


class Whisper(cmd.Cmd):
    os.system('clear')
    intro = "Welcome to WhisperCast! Type 'help' to list commands."
    prompt = "\n(whisper) "

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
        """
        Teach the user about a file and allow them to ask questions.
        """
        if not arg.strip():
            logger.error("No file provided. Please specify a file.")
            print("Usage: sensei <file_path>")
            return

        file_path = arg.strip()
        if not os.path.isfile(file_path):
            logger.error(f"File not found: {file_path}")
            print(f"File not found: {file_path}")
            return

        logger.info(f"Extracting content from file: {file_path}")
        content = extract_content(file_path)

        if not content:
            logger.error("Failed to extract content from the file.")
            print("Failed to extract content from the file.")
            return

        # Split content into manageable chunks
        content_chunks = split_content_for_llm(content)
        print("\nYou can now ask questions about the file. Type 'exit' to quit Sensei mode.")
        while True:
            question = input("\nYour question: ").strip()
            if question.lower() == "exit":
                print("Exiting Sensei mode.")
                break

            try:
                logger.info(f"Processing question: {question}")
                client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

                # Process each chunk and aggregate answers
                aggregated_answer = []
                for i, chunk in enumerate(content_chunks):
                    prompt = f"""
                        You are an expert teacher. Based on the following content, answer the user's question:

                        Content:
                        \"\"\"{chunk}\"\"\"

                        Question:
                        \"\"\"{question}\"\"\"

                        Provide a clear and concise answer.
                    """
                    response = client.chat.completions.create(
                        model="llama3-70b-8192",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=512
                    )
                    answer = response.choices[0].message.content.strip()
                    aggregated_answer.append(answer)

                # Combine answers from all chunks
                final_answer = "\n".join(aggregated_answer)
                print(f"\nAnswer: {final_answer}")
            except Exception as e:
                logger.error(f"Error while answering question: {e}")
                print("An error occurred while processing your question. Please try again.")

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

def split_content_for_llm(content: str, max_tokens: int = 6000) -> list:
    """
    Split content into smaller chunks to fit within the token limit.
    """
    words = content.split()
    chunk_size = max_tokens // 2  # Approximate words per chunk
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
