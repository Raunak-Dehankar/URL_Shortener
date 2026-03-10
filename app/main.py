from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.url_service import create_short_url, get_original_url
from app.schemas import URLRequest
from fastapi import HTTPException

app = FastAPI()

@app.get("/")
def home():
    return {"message": "URL Shortener API"}


@app.post("/shorten")
def shorten_url(request: URLRequest):
    code = create_short_url(request.url)
    return {"short_url": f"http://localhost:8000/{code}"}

@app.get("/{short_code}")
def redirect(short_code: str):
    original_url = get_original_url(short_code)

    if not original_url:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(original_url)