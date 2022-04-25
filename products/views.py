from django.shortcuts import render,redirect
from django.views import View
from django.conf import settings
import stripe
from django.http import JsonResponse
stripe.api_key=settings.STRIP_PRIVATE_KEY
# This is your test secret API key.
class CheckOutSessionView(View):
    def post(self,request):
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
        return JsonResponse({
            'id':checkout_session.id
        })

class checkout(View):
    def get(self,request):
        return render(request,'checkout.html')
