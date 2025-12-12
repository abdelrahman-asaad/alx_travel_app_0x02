# tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_payment_confirmation_email(user_email, booking_id):
    send_mail(
        "Booking Confirmed",
        f"Your booking {booking_id} is confirmed and payment received.",
        "from@example.com",
        [user_email]
    )
