"""Simple test version of the bot for Railway deployment."""

import os
from fastapi import FastAPI

print("Starting simple app...")
print(f"PORT: {os.environ.get('PORT', 'Not set')}")

app = FastAPI(title="Location Bot Simple", version="1.0.0")

@app.get("/")
async def root():
    return {
        "status": "ok", 
        "message": "Simple version is working!",
        "port": os.environ.get('PORT', '8000')
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 