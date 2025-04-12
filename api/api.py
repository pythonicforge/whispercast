from fastapi import FastAPI
from router import router 


app = FastAPI(title="WhisperCast API ⚡️")

@app.get("/")
def index():
    return {
        'message':'Hello! Welcome to WhisperCast. Visit "/docs" for API documentation'
    }

app.include_router(router=router)