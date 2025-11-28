from datetime import datetime
from vip.activate import user_vip

def is_vip(user_id):
    """بررسی اینکه کاربر VIP هست یا نه"""
    if user_id not in user_vip:
        return False

    expire = datetime.strptime(user_vip[user_id]["expire"], "%Y-%m-%d")
    return expire >= datetime.now()
