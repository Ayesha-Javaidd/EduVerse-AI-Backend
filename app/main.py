from fastapi import FastAPI

app = FastAPI(title="EduVerse AI Backend")

@app.get("/")
def root():
    return {"message" : "Success !"}