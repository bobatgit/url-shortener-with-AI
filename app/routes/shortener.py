from fastapi import APIRouter, HTTPException
from app.models import URLCreate, URLResponse
from app.database import get_db
from app.utils.url_utils import generate_short_code

router = APIRouter()

@router.post("/shorten", response_model=URLResponse)
async def create_short_url(url_data: URLCreate):
    with get_db() as db:
        short_code = url_data.custom_code or generate_short_code()
        db.execute(
            "INSERT INTO urls (short_code, original_url, title) VALUES (?, ?, ?)",
            (short_code, str(url_data.url), url_data.title)
        )
        db.commit()
        result = db.execute("SELECT * FROM urls WHERE short_code = ?", (short_code,)).fetchone()
        return dict(result)

@router.get("/{short_code}")
async def redirect_to_url(short_code: str):
    with get_db() as db:
        result = db.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,)).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="URL not found")
        db.execute("UPDATE urls SET click_count = click_count + 1 WHERE short_code = ?", (short_code,))
        db.commit()
        return {"url": result["original_url"]}