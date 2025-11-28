def organs_analysis(warm, cold, dry, wet):
    result = ""

    if warm > cold:
        result += "قلب، کبد و عضلات شما فعال‌تر و پرانرژی‌تر هستند.\n"
    else:
        result += "مغز، معده و کلیه‌ها تمایل به کندی و آرامی دارند.\n"

    if dry > wet:
        result += "پوست، مفاصل و سیستم عصبی شما خشک‌تر و حساس‌تر هستند.\n"
    else:
        result += "سیستم گوارش، ریه‌ها و پوست شما مرطوب‌تر و نرم‌تر عمل می‌کنند.\n"

    return result
