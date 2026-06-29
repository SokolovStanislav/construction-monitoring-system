from fastapi import FastAPI

app = FastAPI(title="Construction Monitoring API")

@app.get("/")
async def root():
    return {"message": "Construction Monitoring System API"}

@app.get("/health")
async def health():
    return {"status": "ok"}
