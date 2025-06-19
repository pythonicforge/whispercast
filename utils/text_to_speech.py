import os
import datetime
import torch
from TTS.api import TTS
from utils import logger
from pydub import AudioSegment
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, Xtts, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig

torch.serialization.add_safe_globals([
    XttsConfig,
    XttsAudioConfig,
    Xtts,
    BaseDatasetConfig,
    XttsArgs
])

@logger.catch
def generate_audio_file(content: str, title: str) -> str:
    """
    Generate an audio file from the given content using TTS and stitch with intro & outro music.
    """
    try:
        if not content.strip():
            raise ValueError("Content for TTS generation is empty.")
        if len(content.split()) < 10:
            raise ValueError("Content is too short for TTS generation.")

        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
        import logging as tts_logging
        tts_logging.getLogger("TTS").setLevel(tts_logging.ERROR)

        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info("Created output directory.")

        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        clean_title = title.lower().replace(" ", "_")
        base_filename = f"{clean_title}_{timestamp}"
        voice_path = os.path.join(output_dir, f"{base_filename}_voice.wav")
        final_output_path = os.path.join(output_dir, f"{base_filename}_final.mp3")

        logger.info("Initializing Text-to-Speech engine...")
        logger.info("Generating podcast audio... please wait.")

        tts = TTS(
            model_name="tts_models/en/ljspeech/glow-tts",
            progress_bar=False,
            gpu=False
        )
        tts.tts_to_file(text=content, file_path=voice_path)

        intro = AudioSegment.from_mp3("utils/intro.mp3").fade_out(1500)
        outro = AudioSegment.from_mp3("utils/intro.mp3").fade_in(1500)
        voice = AudioSegment.from_wav(voice_path)

        final_audio = intro + voice + outro
        final_audio.export(final_output_path, format="mp3")

        logger.success(f"Final podcast saved as: {final_output_path}")
        return final_output_path

    except ValueError as ve:
        logger.error(f"TTS generation failed: {ve}")
        return ""
    except Exception as e:
        logger.critical(f"Error during TTS generation: {e}")
        return ""
