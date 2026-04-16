import subprocess
from datetime import datetime
from app.database import get_max_post_id
from scripts.run_crawler import sync_images_to_db

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def run():
    log("开始增量爬图")
    tags = ["yamada_ryo"]
    max_id = get_max_post_id()
    log(f"本地最大ID: {max_id}")

    for tag in tags:
        log(f"抓取标签: {tag}")

        # ✅ 终极修复：利用 Danbooru 搜索语法实现真正的增量拉取
        search_query = f"{tag}"
        if max_id > 0:
            # 增加 +order:id 强制按 ID 正序（从旧到新）拉取，防止新图过多导致漏图
            search_query += f"+id:>{max_id}+order:id"
            
        url = f"https://danbooru.donmai.us/posts?tags={search_query}"

        # 使用 subprocess 替代 os.system 以获得更好的异常捕获能力
        cmd = ["gallery-dl", "--range", "1-50", url]
        log(f"执行命令: {' '.join(cmd)}")
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            log(f"爬取进程执行异常: {e}")

    log("开始入库")
    # 直接调用 Python 函数，避免通过 os.system 启动新解释器
    sync_images_to_db()

    log("任务完成")

if __name__ == "__main__":
    run()