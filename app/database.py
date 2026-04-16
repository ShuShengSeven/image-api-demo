import sqlite3
import os
import re

DB_PATH = "data/images.db"


# =====================
# 初始化数据库
# =====================
def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
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
    conn.close()


# =====================
# 提取 post_id
# =====================
def extract_post_id(path):
    match = re.search(r'danbooru_(\d+)', path)
    return int(match.group(1)) if match else None


# =====================
# 入库（增量核心）
# =====================
def insert_image(tag, path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    post_id = extract_post_id(path)

    cursor.execute(
        """
        INSERT OR IGNORE INTO images (tag, path, post_id)
        VALUES (?, ?, ?)
        """,
        (tag, path, post_id)
    )

    conn.commit()
    conn.close()


# =====================
# 获取最大ID（增量核心）
# =====================
def get_max_post_id():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(post_id) FROM images")
    result = cursor.fetchone()[0]

    conn.close()
    return result or 0


# =====================
# 随机取图 API
# =====================
def get_random_image(tag):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if tag == "%":
        cursor.execute(
            "SELECT path FROM images ORDER BY RANDOM() LIMIT 1"
        )
    else:
        cursor.execute(
            "SELECT path FROM images WHERE tag=? ORDER BY RANDOM() LIMIT 1",
            (tag,)
        )

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None