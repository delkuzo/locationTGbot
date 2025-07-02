"""Minimal FastAPI app for testing Railway deployment."""

import os
from fastapi import FastAPI
import uvicorn

print("Starting minimal app...")
print(f"Environment: {os.environ.get('ENVIRONMENT', 'production')}")
print(f"Port: {os.environ.get('PORT', '8000')}")

app = FastAPI(title="Location Bot Test", version="1.0.0")

@app.get("/")
async def root():
    return {
        "status": "ok", 
        "message": "Minimal app is running",
        "port": os.environ.get('PORT', '8000')
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "location-bot-minimal"}

@app.get("/env")
async def env_info():
    return {
        "cwd": os.getcwd(),
        "port": os.environ.get('PORT', 'Not set'),
        "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}",
        "environment": os.environ.get('ENVIRONMENT', 'Not set')
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 