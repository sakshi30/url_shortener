import os
from time import time
from fastapi import FastAPI
from dotenv import load_dotenv
from database import Database
from shortener import Shortener
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
import uvicorn

load_dotenv()

app = FastAPI(title="URL Shortener", version="1.0.0")
database = Database()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'message': 'Hello From URL shortner'
    }

@app.post("/shorten-url")
async def process_url(request: Request):
    """Shorten a url and save it in mongodb"""
    try:
        body = await request.json()
        final_destination = body["url"]
        short_key = Shortener.encode_url(final_destination)
        short_url = f"{os.getenv("DOMAIN")}/{short_key}"
        document = {
           "short_url": short_url,
           "long_url": final_destination,
           "created_at": time()
        }
        inserted = database.insert_document(document, os.getenv("SHORTURL_COLLECTION"))
        if inserted:
            return JSONResponse(status_code=200, content={"status": "success", "short_url": short_url})
        else:
            raise HTTPException(status_code=500, detail="Insertion failed")
    except Exception as e:
         return JSONResponse(status_code=400, content={"status": "error", "detail": str(e)})

@app.get("/{short_url}")
async def process_shorturl(short_url: str, request: Request):
    """Redirect the user to the final destination and store the event in database for future monitoring"""
    short_key =  f"{os.getenv("DOMAIN")}/{short_url}"
    document = {"short_url": short_key}
    response = database.get_document(document, os.getenv("SHORTURL_COLLECTION"))
    if response["long_url"]:
        click_event = {
            "short_key": short_key,
            "timestamp": time(),
            "ip": request.headers.get("host"),
            "user_agent": request.headers.get("user-agent"),
            "referrer": request.headers.get("referer"),
        }
        database.insert_document(click_event, os.getenv("EVENT_COLLECTION"))
        return RedirectResponse(response["long_url"])
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")

if __name__ == "__main__":
    print("🚀 Starting Agentic RAG Finance Tracker")
    print("\n🌐 Server will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)