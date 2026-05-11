from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World: DevOps Edition"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}