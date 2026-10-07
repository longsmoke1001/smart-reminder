# Smart Reminder

An AI-powered reminder system that lets you set reminders using natural language through Discord.

Type `/remind tomorrow at 9am remind me to buy groceries` — the AI parses it, stores it, and sends you a Discord notification when it's due.
---

## Features

- Natural language parsing (Chinese & English)
- Discord slash commands: `/remind`, `/list`, `/delete`
- Background scheduler checks every minute
- Discord notifications when reminders are due
- Recurring reminders (every X seconds/minutes/hours)
- SQLite storage via SQLAlchemy
- REST API with Swagger UI (`/docs`)
---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.13 |
| Web framework | FastAPI |
| Discord bot | discord.py |
| AI/LLM | NVIDIA NIM / OpenRouter (OpenAI-compatible) |
| Scheduler | APScheduler |
| Database | SQLite + SQLAlchemy |
| Notifications | Discord Webhook |
---

## Project Structure

```text
smart-reminder/
├── main.py               # FastAPI entry point
├── bot.py                # Discord bot
├── ai_parser.py          # AI parsing logic
├── database.py           # Database models
├── notifier.py           # Discord notifications
├── scheduler.py          # Background scheduler
├── requirements.txt
├── .env.example
└── README.md

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/longsmoke1001/smart-reminder.git
cd smart-reminder
py -3.13 -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
