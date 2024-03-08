from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from . models import Booking


@shared_task
def send_booking_detail_email(user_email, booking_detail):
    try:
        booking = Booking.objects.get(pk=booking_detail)
        subject = 'booking confirm'
        message = 'thank you for booking! you can check detail al link down be low'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [booking.user.email]

        send_mail(subject, message, from_email, recipient_list)
    except Booking.DoesNotExist:
        return None

