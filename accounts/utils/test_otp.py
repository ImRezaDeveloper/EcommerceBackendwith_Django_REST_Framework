# test_otp.py
import random
from django.core.cache import cache
from .otp import OTPHandler   # مسیر رو درست کن

# یه شماره تستی
phone = "09123456789"

# مرحله ۱: تولید OTP
result = OTPHandler.generate_otp(phone)
print("Generate result:", result)

# اگه OTP تولید شد، مقدارش رو ببین (فقط برای تست!)
# توجه: در پروداکشن این خط رو حذف کن
otp_value = cache.get(f"otp_{OTPHandler._get_hashed_phone(phone)}")
print("ذخیره‌شده در کش:", otp_value)

# مرحله ۲: تست تأیید درست
if otp_value:
    verify_correct = OTPHandler.verify_otp(phone, otp_value)
    print("تأیید درست:", verify_correct)

# مرحله ۳: تست تأیید غلط
verify_wrong = OTPHandler.verify_otp(phone, "12345")
print("تأیید غلط:", verify_wrong)

# مرحله ۴: تست تلاش زیاد
print("\nتلاش‌های اشتباه:")
for i in range(5):
    res = OTPHandler.verify_otp(phone, "99999")
    print(f"تلاش {i+1}:", res)