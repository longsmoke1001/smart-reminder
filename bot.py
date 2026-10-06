import os
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv

from ai_parser import parse_reminder
from database import add_reminder

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# 設定 Bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Bot 啟動時跑"""
    print(f"✅ Bot 已登入：{bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ 已同步 {len(synced)} 個斜線指令")
    except Exception as e:
        print(f"❌ 同步失敗：{e}")


@bot.tree.command(name="remind", description="用自然語言設提醒")
@app_commands.describe(text="例如：聽日朝早 9 點提我買餸")
async def remind(interaction: discord.Interaction, text: str):
    """斜線指令 /remind"""
    await interaction.response.defer()  # 等 AI 解析

    try:
        # 用 AI 解析
        parsed = parse_reminder(text)
        reminder_time = datetime.strptime(parsed["time"], "%Y-%m-%d %H:%M")

        # 存入數據庫
        reminder = add_reminder(reminder_time, parsed["message"])

        # 回覆用戶
        await interaction.followup.send(
            f"✅ 已設定提醒！\n"
            f"⏰ 時間：{reminder.time}\n"
            f"📝 內容：{reminder.message}"
        )
    except Exception as e:
        await interaction.followup.send(f"❌ 解析失敗：{e}")


@bot.tree.command(name="list", description="睇所有提醒")
async def list_reminders(interaction: discord.Interaction):
    """斜線指令 /list"""
    from database import get_all_reminders

    reminders = get_all_reminders()

    if not reminders:
        await interaction.response.send_message("📭 冇任何提醒")
        return

    message = "📋 **所有提醒：**\n"
    for r in reminders:
        status = "✅" if r.sent else "⏳"
        message += f"{status} `{r.id}` {r.time} - {r.message}\n"

    await interaction.response.send_message(message)


@bot.tree.command(name="delete", description="刪除提醒")
@app_commands.describe(reminder_id="提醒 ID")
async def delete_reminder(interaction: discord.Interaction, reminder_id: int):
    """斜線指令 /delete"""
    from database import delete_reminder as db_delete

    success = db_delete(reminder_id)

    if success:
        await interaction.response.send_message(f"✅ 已刪除提醒 `{reminder_id}`")
    else:
        await interaction.response.send_message(f"❌ 搵唔到提醒 `{reminder_id}`")


if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)