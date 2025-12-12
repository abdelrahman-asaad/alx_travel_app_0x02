import os
import requests
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Payment, Booking

CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")
CHAPA_INIT_URL = "https://api.chapa.co/v1/transaction/initialize"
CHAPA_VERIFY_URL = "https://api.chapa.co/v1/transaction/verify/"

@api_view(['POST'])
def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    data = {
        "amount": float(booking.amount),
        "currency": "ETB",
        "email": booking.user.email,
        "first_name": booking.user.first_name,
        "last_name": booking.user.last_name,
        "tx_ref": f"booking_{booking.id}",
        "callback_url": "https://yourdomain.com/payment/verify/"
    }
    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
    resp = requests.post(CHAPA_INIT_URL, json=data, headers=headers)
    res_data = resp.json()
    
    payment = Payment.objects.create(
        booking=booking,
        transaction_id=res_data.get("data", {}).get("id"),
        status="Pending",
        amount=booking.amount
    )
    return Response(res_data)
@api_view(['GET'])
def verify_payment(request, transaction_id):
    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
    resp = requests.get(f"{CHAPA_VERIFY_URL}{transaction_id}", headers=headers)
    res_data = resp.json()

    payment = get_object_or_404(Payment, transaction_id=transaction_id)
    
    if res_data.get("data", {}).get("status") == "success":
        payment.status = "Completed"
        # هنا ممكن تستدعي Celery لإرسال الإيميل
    else:
        payment.status = "Failed"

    payment.save()
    return Response(res_data)
# listings/views.py
from .tasks import send_payment_confirmation_email

@api_view(['GET'])
def verify_payment(request, transaction_id):
    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
    resp = requests.get(f"{CHAPA_VERIFY_URL}{transaction_id}", headers=headers)
    res_data = resp.json()

    payment = get_object_or_404(Payment, transaction_id=transaction_id)

    if res_data.get("data", {}).get("status") == "success":
        payment.status = "Completed"
        payment.save()

        # استدعاء Celery task لإرسال الإيميل
        send_payment_confirmation_email.delay(
            user_email=payment.booking.user.email,
            booking_id=payment.booking.id
        )
    else:
        payment.status = "Failed"
        payment.save()

    return Response(res_data)
