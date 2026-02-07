from celery import shared_task
from django.core.mail import send_mail
import time


@shared_task
def send_test_email(user_email, user_name):
    print(f"تسک شروع شد برای {user_email}")
    time.sleep(5)
    subject = "خوش آمدید به فروشگاه ما!"
    message = f"‍سلام {user_name} 👋، به فروشگاه ما خوش آمدید!"
    from_email = "noreply@example.com"
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[user_email],
            fail_silently=False,
        )
        print("ایمیل با موفقیت ارسال شد")
        return f'email sent to {user_email}'
    except Exception as e:
        print(f"خطا در ارسال ایمیل: {e}")
        raise