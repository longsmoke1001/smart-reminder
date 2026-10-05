# Smart Reminder

An AI-powered reminder system that lets you set reminders using natural language through Discord.

Type `/remind tomorrow at 9am remind me to buy groceries` — the AI parses it, stores it, and sends you a Discord notification when it's due.

---

## Features

- Natural language parsing (Chinese & English)
- Discord slash commands: `/remind`, `/list`, `/delete`
- Background scheduler checks every minute
- Discord notifications when reminders are due
- SQLite storage via SQLAlchemy
- REST API with Swagger UI (`/docs`)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.13 |
| Web framework | FastAPI |
| Discord bot | discord.py |
| AI/LLM | NVIDIA NIM (OpenAI-compatible) |
| Scheduler | APScheduler |
| Database | SQLite + SQLAlchemy |
| Notifications | Discord Webhook |

---

## Project Structure
