from apscheduler.schedulers.background import BackgroundScheduler
from database import get_due_reminders, mark_as_sent
from notifier import send_discord_notification

scheduler = BackgroundScheduler()


def check_reminders():
    """檢查有冇到期提醒，到期就發送通知"""
    due_reminders = get_due_reminders()

    if not due_reminders:
        return

    print(f"搵到 {len(due_reminders)} 個到期提醒")

    for reminder in due_reminders:
        print(f"發送提醒：{reminder.message}")
        success = send_discord_notification(reminder.message)

        if success:
            mark_as_sent(reminder.id)
            print(f"✅ 已發送並標記：{reminder.id}")
        else:
            print(f"❌ 發送失敗：{reminder.id}")


def start_scheduler():
    """啟動定時任務"""
    scheduler.add_job(
        check_reminders,
        "interval",
        minutes=1,
        id="check_reminders",
        replace_existing=True,
    )
    scheduler.start()
    print("✅ Scheduler 已啟動，每分鐘檢查一次")


def stop_scheduler():
    """停止定時任務"""
    if scheduler.running:
        scheduler.shutdown()
        print("🛑 Scheduler 已停止")


if __name__ == "__main__":
    import time
    from datetime import datetime, timedelta
    from database import add_reminder

    # 測試：新增一個 10 秒後到期嘅提醒
    test_time = datetime.now() + timedelta(seconds=10)
    reminder = add_reminder(test_time, "測試定時提醒")
    print(f"新增提醒：{reminder}")

    # 啟動 scheduler
    start_scheduler()

    # 跑 60 秒俾佢檢查
    try:
        time.sleep(60)
    except KeyboardInterrupt:
        pass
    finally:
        stop_scheduler()