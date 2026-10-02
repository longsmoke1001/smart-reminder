import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# 讀取供應商設定（預設 nvidia）
PROVIDER = os.getenv("AI_PROVIDER", "nvidia")


def call_ai(prompt: str) -> str:
    """統一介面，內部切換供應商"""
    if PROVIDER == "nvidia":
        return call_nvidia(prompt)
    elif PROVIDER == "gemini":
        return call_gemini(prompt)
    elif PROVIDER == "groq":
        return call_groq(prompt)
    elif PROVIDER == "claude":
        return call_claude(prompt)
    else:
        raise ValueError(f"Unknown provider: {PROVIDER}")


def call_nvidia(prompt: str) -> str:
    """用 NVIDIA NIM API（兼容 OpenAI 格式）"""
    from openai import OpenAI

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.getenv("NVIDIA_API_KEY"),
    )

    model = os.getenv("NVIDIA_MODEL", "meta/llama-3.3-70b-instruct")

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1024,
    )

    return response.choices[0].message.content


def call_gemini(prompt: str) -> str:
    """用 Google Gemini API"""
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text


def call_groq(prompt: str) -> str:
    """用 Groq API（免費、極快）"""
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def call_claude(prompt: str) -> str:
    """用 Anthropic Claude API"""
    import anthropic

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def parse_reminder(user_input: str, retries: int = 3) -> dict:
    """用 AI 將自然語言轉做結構化資料（有 retry）"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    prompt = f"""現在時間：{now}
將以下句子轉做 JSON，只回傳 JSON：
"{user_input}"

格式：{{"time": "YYYY-MM-DD HH:MM", "message": "內容"}}
"""

    for attempt in range(retries):
        try:
            text = call_ai(prompt)
            if text is None:
                continue
            text = text.strip()

            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]

            return json.loads(text.strip())
        except Exception as e:
            print(f"第 {attempt + 1} 次失敗：{e}")
            if attempt == retries - 1:
                raise

    raise ValueError("重試多次仍然失敗")


if __name__ == "__main__":
    # 測試
    test_inputs = [
        "聽日朝早 9 點提我買餸",
        "下個禮拜一 3pm 開會",
        "今晚 8 點提醒我睇波",
    ]

    for text in test_inputs:
        print(f"輸入：{text}")
        try:
            result = parse_reminder(text)
            print(f"輸出：{result}")
        except Exception as e:
            print(f"錯誤：{e}")
        print("-" * 40)