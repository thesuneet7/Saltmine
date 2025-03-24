from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
import os



app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
