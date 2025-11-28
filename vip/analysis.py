from vip.organs import organs_analysis
from vip.strengths import strengths_and_weaknesses
from vip.lifestyle import lifestyle_tips
from vip.nutrition import nutrition_tips

def advanced_analysis(result):
    warm = result["warm"]
    cold = result["cold"]
    dry = result["dry"]
    wet = result["wet"]

    text = f"""
🌟 تحلیل پیشرفته مزاج شما

🌡️ گرمی: {warm}٪  
❄️ سردی: {cold}٪  
🌵 خشکی: {dry}٪  
💧 تری: {wet}٪  

این یعنی بدن شما بیشتر به سمت «گرمی و خشکی» متمایل است؛
بدنی که انرژی، سرعت و قدرت تصمیم‌گیری بالایی دارد،
اما در عین حال نیاز دارد کمی آرام‌تر، خنک‌تر و مرطوب‌تر زندگی کند.

────────────────────

🧠 تحلیل اعضای بدن:
{organs_analysis(warm, cold, dry, wet)}

────────────────────

✅ نقاط قوت و ضعف:
{strengths_and_weaknesses(warm, cold, dry, wet)}

────────────────────

🍃 توصیه‌های سبک زندگی:
{lifestyle_tips(warm, cold, dry, wet)}

────────────────────

🍽️ تغذیه مناسب:
{nutrition_tips(warm, cold, dry, wet)}
"""

    return text
