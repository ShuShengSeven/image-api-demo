import os
from app.database import init_db, insert_image

init_db()

image_dir = "gallery-dl"

count = 0

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
            path = os.path.join(root, file)

            # 🔥 关键：自动提取tag（最后一层文件夹名）
            tag = os.path.basename(root)

            insert_image(tag, path)
            count += 1

print(f"已入库 {count} 张图片")