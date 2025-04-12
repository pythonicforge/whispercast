import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import logger
from typing import Optional
from fastapi import Query, HTTPException, APIRouter
from services import generate_from_topic, generate_from_content


router = APIRouter(prefix='/generate', tags=['Podcast Generation'])

@logger.catch
@router.get('/')
def generate_podcast(
    topic: Optional[str] = Query(default=None),
    content: Optional[str] = Query(default=None)
):
    logger.info(f"Received request with topic: {topic}, content: {content}")
    
    if topic and not content:
        response = generate_from_topic(topic=topic)
        logger.info(f"Response from generate_from_topic: {response}")
        return response
    elif content and not topic:
        response = generate_from_content(content=content)
        logger.info(f"Response from generate_from_content: {response}")
        return response
    elif topic and content:
        logger.error("Both 'topic' and 'content' provided. Raising HTTPException.")
        raise HTTPException(status_code=400, detail="You must pass either a 'topic' or 'content' to generate a podcast, not both!")
    else:
        logger.error("Neither 'topic' nor 'content' provided. Raising HTTPException.")
        raise HTTPException(status_code=400, detail="You must either pass a 'topic' or 'content' to generate a podcast.")