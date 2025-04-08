import os
import datetime
from TTS.api import TTS
from utils import logger
import torch
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, Xtts, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig

# Allowlist all necessary XTTS-related globals
torch.serialization.add_safe_globals([
    XttsConfig,
    XttsAudioConfig,
    Xtts, 
    BaseDatasetConfig, 
    XttsArgs

])
@logger.catch
def generate_audio_file(content: str, title: str) -> str:
    try:
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
        import logging as tts_logging
        tts_logging.getLogger("TTS").setLevel(tts_logging.ERROR)

        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info("Created output directory.")

        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        clean_title = title.lower().replace(" ", "_")
        filename = f"{clean_title}_{timestamp}.wav"
        output_path = os.path.join(output_dir, filename)

        logger.info("Initializing Text-to-Speech engine...")

        logger.info("Generating podcast audio... please wait.")

        tts = TTS(
            model_name="tts_models/en/ljspeech/glow-tts",
            progress_bar=False,
            gpu=False
        )
     #    tts.synthesizer.tts_config.decoder_params["max_decoder_steps"] = 40000

        tts.tts_to_file(text=content, file_path=output_path)

        logger.success(f"Audio saved at: {output_path}")

        return output_path

    except Exception as e:
        logger.critical(f"Error during TTS generation: {e}")
        return ""
