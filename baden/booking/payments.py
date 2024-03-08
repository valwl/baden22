import stripe
from . models import Booking
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from . task import send_booking_detail_email

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_195c26f45444306cee6808fa8bbee24cbf73f72482cab20bb44349a52c69e12f'

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


class PaymentHandler:
    def __init__(self, endpoint_secret):
        self.endpoint_secret = endpoint_secret

    @csrf_exempt
    def webhook_view(self, request):
        payload = request.body.decode('utf-8')
        sig_header = request.headers.get('Stripe-Signature')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.endpoint_secret
            )
        except ValueError as e:
            return Response({'status': 'invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.complete':
            session = event['data']['object']
            booking_id = session['cliente_reference_id']
            booking = Booking.objects.get(id=booking_id)
            payment_id = self.confirm_payment(booking)

    def confirmation_payment(self, booking):
        checkout_session = stripe.checkout.Session.retrieve(booking)
        payment_intent = stripe.PaymentIntent.retrieve(checkout_session.payment_intent)

        if payment_intent.status == 'success':
            booking.status = 'paid'
            booking.save()
            send_booking_detail_email.delay(booking.pk)
            return booking

# нужны ли в принципе веб-хуки или достаточно обратиться к PaymentIntent





# @csrf_exempt
# def webhook(request):
#     event = None
#     payload = request.data
#     sig_header = request.headers['STRIPE_SIGNATURE']
#
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         raise e
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         raise e
#
#     # Handle the event
#     if event['type'] == 'payment_intent.succeeded':
#       payment_intent = event['data']['object']
#     # ... handle other event types
#     else:
#       print('Unhandled event type {}'.format(event['type']))
#
#     return jsonify(success=True)
