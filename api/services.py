from fastapi import FastAPI


app = FastAPI(title="WhisperCast API ⚡️")

@app.get("/")
def index():
    return {
        'message':'Hello! Welcome to WhisperCast. Visit "/docs" for API documentation'
    }

