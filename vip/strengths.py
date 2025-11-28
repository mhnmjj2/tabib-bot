def strengths_and_weaknesses(warm, cold, dry, wet):
    result = ""

    if warm > cold:
        result += "✅ انرژی، تحرک، شجاعت و سرعت عمل بالا\n"
    else:
        result += "✅ آرامش، تمرکز، دقت و خونسردی بیشتر\n"

    if dry > wet:
        result += "✅ تحلیل‌گری، منطق، اراده قوی و استقلال\n"
    else:
        result += "✅ انعطاف‌پذیری، همدلی، لطافت و ارتباط‌پذیری\n"

    result += "\n"

    if warm > 70:
        result += "⚠️ ممکن است زودجوش، عصبی یا پرخاشگر باشید\n"
    if cold > 70:
        result += "⚠️ ممکن است کند، بی‌انگیزه یا افسرده شوید\n"
    if dry > 70:
        result += "⚠️ ممکن است سخت‌گیر، منزوی یا خشک‌رفتار باشید\n"
    if wet > 70:
        result += "⚠️ ممکن است بی‌ثبات، وابسته یا احساساتی شوید\n"

    return result
