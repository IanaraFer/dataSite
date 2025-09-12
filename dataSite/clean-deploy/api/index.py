from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AnalyticaCore AI API"}

@app.get("/api/health")
def health():
    return {"status": "healthy"}
