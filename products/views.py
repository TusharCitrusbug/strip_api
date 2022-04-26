import stripe
from django.shortcuts import render,redirect
from django.views import View
from django.conf import settings
from django.http import JsonResponse
from products.models import *
# from products.serializers import
from rest_framework.generics import ListAPIView,GenericAPIView,ListCreateAPIView,RetrieveUpdateAPIView,DestroyAPIView,RetrieveUpdateDestroyAPIView
stripe.api_key=settings.STRIP_PRIVATE_KEY

class CustomerApiView(ListCreateAPIView):
    queryset =Customer.objects.all()
    def post(self, request, *args, **kwargs):
        stripe.Customer.create(balance=request.POST.get('balance'),email=request.POST.get('email'))
        return self.create(request, *args, **kwargs)
    # serializer_class= CustomerSerializer
    pass
# This is your test secret API key.
# class CheckOutSessionView(View):
#     def post(self,request):
#         YOUR_DOMAIN = "http://127.0.0.1:8000"
#         checkout_session = stripe.checkout.Session.create(
#             line_items=[
#                 {
#                     'price': '{{PRICE_ID}}',
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#             # success_url=YOUR_DOMAIN + '/success',
#             # cancel_url=YOUR_DOMAIN + '/cancel',
#         )
#         return JsonResponse({
#             'id':checkout_session.id
#         })

# class checkout(View):
#     def get(self,request):
#         return render(request,'checkout.html')
