from fastapi import FastAPI, File, UploadFile, Form
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Server is running"}

@app.post("/api/trial/submit-with-file")
async def submit_trial(
    firstName: str = Form(...),
    lastName: str = Form(...),
    email: str = Form(...),
    businessData: UploadFile = File(None)
):
    file_info = None
    if businessData:
        file_info = {
            "filename": businessData.filename,
            "size": len(await businessData.read())
        }
    
    return {
        "success": True,
        "customer_id": "TEST-123",
        "file_received": bool(file_info),
        "file_info": file_info
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
