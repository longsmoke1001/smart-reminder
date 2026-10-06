FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# This command should start both your bot and your FastAPI app
CMD ["python", "bot.py"]