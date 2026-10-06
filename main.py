from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from contextlib import asynccontextmanager

from ai_parser import parse_reminder
from database import add_reminder, get_all_reminders, delete_reminder
from scheduler import start_scheduler, stop_scheduler


# ===== 啟動 / 關閉事件 =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動時
    start_scheduler()
    yield
    # 關閉時
    stop_scheduler()


app = FastAPI(
    title="Smart Reminder API",
    description="用自然語言設提醒嘅 API",
    version="1.0.0",
    lifespan=lifespan,
)


# ===== Request Model =====
class ReminderRequest(BaseModel):
    text: str


# ===== API Endpoints =====
@app.get("/")
def root():
    return {"message": "Smart Reminder API 運作中"}


@app.post("/reminders")
def create_reminder(req: ReminderRequest):
    """用自然語言建立提醒"""
    try:
        parsed = parse_reminder(req.text)
        reminder_time = datetime.strptime(parsed["time"], "%Y-%m-%d %H:%M")
        reminder = add_reminder(reminder_time, parsed["message"])
        return {
            "id": reminder.id,
            "time": reminder.time,
            "message": reminder.message,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"解析失敗：{e}")


@app.get("/reminders")
def list_reminders():
    """拎所有提醒"""
    reminders = get_all_reminders()
    return [
        {
            "id": r.id,
            "time": r.time,
            "message": r.message,
            "sent": r.sent,
        }
        for r in reminders
    ]


@app.delete("/reminders/{reminder_id}")
def remove_reminder(reminder_id: int):
    """刪除提醒"""
    success = delete_reminder(reminder_id)
    if not success:
        raise HTTPException(status_code=404, detail="搵唔到提醒")
    return {"ok": True}

# main.py 底部加入
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)