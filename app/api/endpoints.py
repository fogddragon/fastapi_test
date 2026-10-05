from fastapi_test.main import app

@app.post("/transform_list")
async def create_transform_list():
    return {"message": "Hello World"}


@app.get("/transform_list/{item_id}")
async def get_tansform_list(item_id: int):
    return {"message": f"Hello {id}"}
