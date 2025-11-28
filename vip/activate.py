from datetime import datetime, timedelta

# دیتابیس ساده VIP
user_vip = {}

ADMIN_ID = 6271244163  # آی‌دی مدیر

def activate_vip(user_id, days=30):
    """فعال‌سازی VIP برای کاربر"""
    expire_date = datetime.now() + timedelta(days=days)
    user_vip[user_id] = {
        "status": True,
        "expire": expire_date.strftime("%Y-%m-%d")
    }
    return expire_date.strftime("%Y-%m-%d")


def is_admin(user_id):
    return user_id == ADMIN_ID
