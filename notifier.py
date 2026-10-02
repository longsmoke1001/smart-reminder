import os
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_discord_notification(message: str) -> bool:
    """用 Discord Webhook 發送通知"""
    if not DISCORD_WEBHOOK_URL:
        print("錯誤：DISCORD_WEBHOOK_URL 未設定")
        return False

    payload = {
        "content": f"⏰ **Reminder:** {message}",
        "username": "Smart Reminder"  # ← 加呢行
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"發送失敗：{e}")
        return False


def send_email_notification(message: str) -> bool:
    """（可選）用 Email 發送通知"""
    # 將來可以加
    pass


if __name__ == "__main__":
    # 測試
    result = send_discord_notification("測試提醒：買餸")
    if result:
        print("✅ 發送成功")
    else:
        print("❌ 發送失敗")