from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Reminder(Base):
    """提醒模型"""
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, nullable=False)
    message = Column(String, nullable=False)
    sent = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Reminder(id={self.id}, time={self.time}, message='{self.message}', sent={self.sent})>"


# 建立 SQLite 數據庫
engine = create_engine("sqlite:///reminders.db", echo=False)
Base.metadata.create_all(engine)

# Session 工廠
Session = sessionmaker(bind=engine)


def get_session():
    """拎一個新 session"""
    return Session()


def add_reminder(time, message):
    """新增提醒"""
    session = get_session()
    try:
        reminder = Reminder(time=time, message=message)
        session.add(reminder)
        session.commit()
        session.refresh(reminder)
        return reminder
    finally:
        session.close()


def get_all_reminders():
    """拎所有提醒"""
    session = get_session()
    try:
        return session.query(Reminder).all()
    finally:
        session.close()


def get_due_reminders():
    """拎到期而未發送嘅提醒"""
    from datetime import datetime
    session = get_session()
    try:
        now = datetime.now()
        return session.query(Reminder).filter(
            Reminder.time <= now,
            Reminder.sent == False
        ).all()
    finally:
        session.close()


def mark_as_sent(reminder_id):
    """標記提醒為已發送"""
    session = get_session()
    try:
        reminder = session.query(Reminder).get(reminder_id)
        if reminder:
            reminder.sent = True
            session.commit()
        return reminder
    finally:
        session.close()


def delete_reminder(reminder_id):
    """刪除提醒"""
    session = get_session()
    try:
        reminder = session.query(Reminder).get(reminder_id)
        if reminder:
            session.delete(reminder)
            session.commit()
            return True
        return False
    finally:
        session.close()


if __name__ == "__main__":
    from datetime import datetime, timedelta

    # 測試：新增提醒
    test_time = datetime.now() + timedelta(minutes=5)
    reminder = add_reminder(test_time, "測試提醒")
    print(f"新增：{reminder}")

    # 測試：拎所有提醒
    all_reminders = get_all_reminders()
    print(f"所有提醒：{all_reminders}")

    # 測試：刪除
    delete_reminder(reminder.id)
    print(f"刪除後：{get_all_reminders()}")