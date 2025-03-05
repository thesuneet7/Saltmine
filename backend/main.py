from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

# Include all API routes
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
