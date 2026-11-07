"""
叫醒 Streamlit App 的機器人訪客
------------------------------------------------
做的事情：
1. 自動從投資機長箱的 app.py 抓出所有 .streamlit.app 網址
   （之後機長箱新增卡片，機器人就會自動照顧，不用另外設定）
2. 再加上 urls.txt 裡手動補充的網址（不在機長箱上的 app）
3. 用看不見的瀏覽器真的把每個頁面打開
4. 如果 app 睡著了，就幫你按「Yes, get this app back up!」
5. 有任何一個打不開，就讓 GitHub 寄信通知你
"""

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
PORTAL_FILE = HERE.parent / "app.py"      # 投資機長箱主程式
EXTRA_FILE = HERE / "urls.txt"            # 手動補充清單

STREAMLIT_URL = re.compile(r"https://[A-Za-z0-9.-]+\.streamlit\.app/?")
WAKE_BUTTON = re.compile(r"get this app back up", re.I)

PAGE_TIMEOUT = 60_000      # 打開頁面最多等 60 秒
SETTLE_WAIT = 8_000        # 打開後再等 8 秒，讓 app 連線
AFTER_WAKE_WAIT = 30_000   # 按下叫醒後等 30 秒，讓 app 開機


def normalize(url):
    return url.rstrip("/") + "/"


def load_urls():
    urls = []
    # 1. 機長箱上的所有 Streamlit 網址
    if PORTAL_FILE.exists():
        urls += STREAMLIT_URL.findall(PORTAL_FILE.read_text(encoding="utf-8"))
    # 2. 手動補充（一行一個，# 開頭是註解）
    if EXTRA_FILE.exists():
        for line in EXTRA_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    # 去除重複，保留順序
    seen, result = set(), []
    for u in map(normalize, urls):
        if u not in seen:
            seen.add(u)
            result.append(u)
    return result


def find_wake_button(page):
    """在主頁面和所有內嵌框架裡找叫醒按鈕"""
    for frame in page.frames:
        button = frame.get_by_role("button", name=WAKE_BUTTON)
        if button.count() > 0:
            return button.first
    return None


def visit(page, url):
    page.goto(url, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT)
    page.wait_for_timeout(SETTLE_WAIT)
    button = find_wake_button(page)
    if button is not None:
        button.click()
        page.wait_for_timeout(AFTER_WAKE_WAIT)
        return "😴 原本在睡，已叫醒"
    return "✅ 醒著"


def main():
    urls = load_urls()
    if not urls:
        print("找不到任何網址")
        sys.exit(1)
    print(f"這次要照顧 {len(urls)} 個 app\n")

    failures = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for url in urls:
            try:
                status = visit(page, url)
            except Exception as e:  # 單一 app 出錯，不影響其他 app
                status = f"❌ 失敗：{type(e).__name__}"
                failures.append(url)
            print(f"{status}  {url}", flush=True)
        browser.close()

    print("-" * 40)
    print(f"共 {len(urls)} 個 app，失敗 {len(failures)} 個")
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
