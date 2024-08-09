import requests
from django.conf import settings

def send_telegram_message(message):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    channel_id = settings.TELEGRAM_CHANNEL_ID
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': channel_id,
        'text': message,
        'parse_mode': 'HTML'  # Optional: use 'HTML' or 'Markdown' to format the message
    }
    response = requests.post(url, data=payload)
    return response.json()