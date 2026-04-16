from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from app.database import get_random_image

app = FastAPI()

@app.get("/random")
def random_image(tag: str = Query(default=None)):
    if tag:
        path = get_random_image(tag)
    else:
        path = get_random_image("%")

    if path:
        return FileResponse(path)

    return {"error": "no image found"}