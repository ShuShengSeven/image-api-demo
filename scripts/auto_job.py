import os
from datetime import datetime
from app.database import get_max_post_id

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def run():
    log("开始增量爬图")

    tags = ["yamada_ryo"]

    max_id = get_max_post_id()
    log(f"本地最大ID: {max_id}")

    for tag in tags:
        log(f"抓取标签: {tag}")

        # ✅ 关键修复：限制范围 + 防止全量
        url = f"https://danbooru.donmai.us/posts?tags={tag}&page=1"

        cmd = (
            f'gallery-dl --range 1-50 '
            f'"{url}"'
        )

        log(f"执行: {cmd}")
        os.system(cmd)

    log("开始入库")
    os.system("python -m scripts.run_crawler")

    log("任务完成")


if __name__ == "__main__":
    run()