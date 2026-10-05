import uvicorn
from fastapi import FastAPI

from fastapi_test.app.api.endpoints import router as api_router

app = FastAPI()
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)