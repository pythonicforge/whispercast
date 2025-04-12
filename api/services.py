import os
from fastapi import HTTPException
from fastapi.responses import FileResponse
from utils import logger, fetch_topic_data, generate_podcast_script, generate_audio_file

@logger.catch
def generate_from_topic(topic: str):
    logger.info(f"Podcast generation started for topic: {topic}")
    content = fetch_topic_data(topic)
    if not content:
        logger.error("No content fetched for the topic.")
        raise HTTPException(status_code=500, detail="Failed to fetch content for the topic.")
    
    logger.info("Generating podcast script...")
    content = generate_podcast_script(topic, content, 5)
    if not content:
        logger.error("Failed to generate podcast script.")
        raise HTTPException(status_code=500, detail="Failed to generate podcast script.")
    
    logger.info("Generating audio file...")
    file_path = generate_audio_file(content, topic.capitalize())
    if not file_path:
        logger.error("Failed to generate audio file.")
        raise HTTPException(status_code=500, detail="Failed to generate audio file.")
    
    logger.success(f"Podcast generation completed. File path: {file_path}")
    return FileResponse(path=file_path, media_type="audio/mpeg", filename=os.path.basename(file_path))

@logger.catch
def generate_from_content(content: str):
    logger.info(f"Podcast generation started for content: {content[:50]}...")
    if not content.strip():
        logger.error("Content is empty.")
        raise HTTPException(status_code=400, detail="Content cannot be empty.")
    
    result = f"Generated podcast from content: {content[:50]}..."
    logger.success(f"Podcast generation completed for content.")
    return {"type": "content", "input": content, "result": result}