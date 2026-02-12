import hashlib
import hmac
import random

from django.conf import settings
from django.core.cache import cache

class OTPHandler:
    
    PHONE_SECRET_KEY = settings.PHONE_SECRET_KEY
    OTP_TIMEOUT = 120
    MAX_ATTEMPTS = 3
    
    @staticmethod
    def _get_hashed_phone(cls, phone_number):
        return hmac.new(
            OTPHandler.PHONE_SECRET_KEY.encode(),
            phone_number.encode(),
            hashlib.sha256
        ).hexdigest()
        
    @staticmethod
    def generate_otp(cls, phone_number):
        hashed_phone = cls._get_hashed_phone(phone_number)
        key = f'otp_{hashed_phone}'
        
        if cache.get(key):
            return {
                "status": "pending",
                "message": "OTP already sent. Please wait 2 minutes."
            }
            
        cache.delete(f"otp_attempts_{hashed_phone}")
        
        otp = str(random.randint(100000, 999999))
        cache.set(key, otp, timeout=cls.OTP_TIMEOUT)
        
        return {
            "status": "success",
            "message": "OTP sent successfully",
            "otp": otp 
        }
        
    @staticmethod
    def verify_otp(cls, phone_number, otp_code):
        hashed_phone = cls._get_hashed_phone(phone_number)
        otp_key = f'otp_{hashed_phone}'
        attempts_key = f"otp_attempts_{hashed_phone}"
        
        stored_otp = cache.get(otp_key)
        
        if not stored_otp:
            return {
                "status": "expired",
                "message": "OTP expired or not found. Request a new one."
            }
            
        attempts = cache.incr(attempts_key)
        
        if attempts == 1:
            cache.expire(attempts_key, cls.OTP_TIMEOUT)
            
        if attempts > cls.MAX_ATTEMPTS:
            cache.delete(otp_key)
            return {
                "status": "blocked",
                "message": f"Too many attempts ({cls.MAX_ATTEMPTS}). Try again after 2 minutes."
            }
            
        if stored_otp == otp_code:
            cache.delete(otp_code)
            cache.delete(attempts_key)
            return {
                "status": "valid",
                "message": "OTP verified successfully"
            }
        
        return {
            "status": "invalid",
            "message": f"Invalid OTP ({attempts}/{cls.MAX_ATTEMPTS} attempts)"
        }