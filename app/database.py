import sqlite3
import os
import re

DB_PATH = "data/images.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT,
            path TEXT UNIQUE,
            post_id INTEGER UNIQUE
        )
        """)
        conn.commit()

def extract_post_id(path):
    # 优化：放宽正则限制，兼容形如 "123456.jpg" 或 "danbooru_123456.jpg" 的情况
    filename = os.path.basename(path)
    match = re.search(r'(?:danbooru_)?(\d+)', filename)
    return int(match.group(1)) if match else None

def insert_images_batch(image_data_list):
    """批量入库（性能核心）"""
    if not image_data_list:
        return
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.executemany(
            """
            INSERT OR IGNORE INTO images (tag, path, post_id)
            VALUES (?, ?, ?)
            """,
            image_data_list
        )
        conn.commit()

def get_max_post_id():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(post_id) FROM images")
        result = cursor.fetchone()[0]
        return result or 0

def get_random_image(tag):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        if tag == "%":
            cursor.execute("SELECT path FROM images ORDER BY RANDOM() LIMIT 1")
        else:
            cursor.execute("SELECT path FROM images WHERE tag=? ORDER BY RANDOM() LIMIT 1", (tag,))
        row = cursor.fetchone()
        return row[0] if row else None

def delete_image_record(path):
    """删除数据库中已丢失物理文件的记录"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM images WHERE path=?", (path,))
        conn.commit()