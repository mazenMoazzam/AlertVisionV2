from fastapi import FastAPI
from routes import feeds, detections, health

app = FastAPI(title="AlertVision Control Plane", version="1.0")

app.include_router(feeds.router, prefix="/feeds", tags=["Feeds"])
app.include_router(detections.router, prefix="/detections", tags=["Detections"])
app.include_router(health.router, prefix="/health", tags=["Health"])

@app.get("/")
def root():
    return {"message": "AlertVision Control Plane is running"}
