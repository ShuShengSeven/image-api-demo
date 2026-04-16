import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from app.database import get_random_image, delete_image_record

app = FastAPI()

@app.get("/random")
def random_image(tag: str = Query(default=None)):
    max_retries = 3  # 设置最大重试次数，防止陷入死循环
    
    for _ in range(max_retries):
        if tag:
            path = get_random_image(tag)
        else:
            path = get_random_image("%")

        if not path:
            return {"error": "no image found in database"}

        # ✅ 优化：校验文件状态，处理数据库有记录但文件已丢失的“脏数据”情况
        if os.path.exists(path):
            return FileResponse(path)
        else:
            delete_image_record(path)
            
    raise HTTPException(status_code=404, detail="Valid image not found. Database might need cleanup.")