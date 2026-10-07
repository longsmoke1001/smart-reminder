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
```

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/longsmoke1001/smart-reminder.git
cd smart-reminder
py -3.13 -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
```

> **Note:** On Mac or Linux, use `source venv/bin/activate` instead.

### 2. Create `.env`

```env
AI_PROVIDER=nvidia
NVIDIA_API_KEY=your_nvidia_api_key
NVIDIA_MODEL=deepseek-ai/deepseek-v4.1-flash

DISCORD_WEBHOOK_URL=your_discord_webhook_url
DISCORD_BOT_TOKEN=your_discord_bot_token
```

| Key | Where to get |
|-----|--------------|
| `NVIDIA_API_KEY` | [build.nvidia.com](https://build.nvidia.com) |
| `DISCORD_WEBHOOK_URL` | Discord channel → Integrations → Webhooks |
| `DISCORD_BOT_TOKEN` | [Discord Developer Portal](https://discord.com/developers/applications) → Bot |

---

## Usage

### Run the Discord bot

```bash
python bot.py
```

### Run the FastAPI server (optional)

```bash
python main.py
```

Visit http://localhost:8000/docs for the API.

---

## Discord Commands

| Command | Description |
|---------|-------------|
| `/remind text: ...` | Set a reminder using natural language |
| `/list` | List all reminders |
| `/delete reminder_id: X` | Delete a reminder by ID |

**Examples:**

```
/remind text: 聽日朝早 9 點提我買餸
/remind text: 下個禮拜一 3pm 開會
/remind text: 今日 8 點提醒我睇波
/remind text: 每 60 秒提醒我飲水
```

---

## How It Works

1. User sends `/remind` in Discord
2. Bot calls `ai_parser.py` → AI parses text into `{ time, message, repeat_seconds }`
3. Reminder stored in SQLite via `database.py`
4. `scheduler.py` checks every minute for due reminders
5. `notifier.py` sends Discord webhook when due
6. If recurring, `reschedule_reminder()` schedules the next occurrence
7. Otherwise, reminder is marked as sent

---

## License

MIT
