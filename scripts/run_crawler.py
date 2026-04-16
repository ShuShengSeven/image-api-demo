import os
from app.database import init_db, insert_images_batch, extract_post_id

def sync_images_to_db(image_dir="gallery-dl"):
    init_db()
    image_data_list = []
    
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
                path = os.path.join(root, file)
                tag = os.path.basename(root)
                post_id = extract_post_id(path)
                
                image_data_list.append((tag, path, post_id))

    if image_data_list:
        insert_images_batch(image_data_list)
        
    print(f"扫描完毕，已向数据库批量提交 {len(image_data_list)} 张图片记录")

if __name__ == "__main__":
    sync_images_to_db()