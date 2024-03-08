from django.db import models
import stripe
from datetime import timedelta
from apartments.models import Apartment
from django.contrib.auth import get_user_model
User = get_user_model()


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    check_in_day = models.DateTimeField()
    check_out_day = models.DateTimeField()
    guest = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=255, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('complete', 'Complete')], default='pending')
    paid = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def calculate_total_price(self):
        # durations = self.check_out_day - self.check_in_day
        current_day = self.check_in_day
        total_cost = 0
        while current_day < self.check_out_day:
            if current_day.weekday() in [5, 6]:
                total_cost += self.apartment.weekend_price
            else:
                total_cost += self.apartment.base_price
            current_day += timedelta(days=1)
        return total_cost

    def set_total_cost(self):
        self.total_price = self.calculate_total_price()

    def create_checkout_session(self):
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': f'{self.total_price}',
                'quantity': 1,
                'name': 'my_booking',
            }],
            mode='payment',
            success_url='https://example.com',
            cancel_url='https://example.com',
            client_refrence_id=str(self.pk),
            payment_intent_data={
                'setup_future_usage': 'off_session',
            },

        )
        return checkout_session

    def __str__(self):
        return f'{self.user.first_name}, {self.apartment.title}, ({self.check_in_day} to {self.check_out_day})'