from asyncio.windows_events import NULL
import webbrowser
import stripe
from django.shortcuts import render,redirect
from django.views import View
from django.conf import settings
from django.http import JsonResponse
from products.models import *
from django.views.decorators.csrf import csrf_exempt
from products.serializers import *
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
stripe.api_key=settings.STRIP_PRIVATE_KEY
from django.contrib.auth.models import User
import jwt
import datetime
from rest_framework.response import Response
from datetime import timedelta
from django.contrib.auth.hashers import make_password,check_password
import requests
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.registration.views import SocialLoginView
from .adapters import GoogleOAuth2AdapterIdToken
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
def jwt_authentication(request):
    try:
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        payload=jwt.decode(jwt_token,'secrate',algorithms=['HS256'])
        return payload
    except:
        return None


class CustomerApiView(ListAPIView):
    queryset =Customer.objects.all()
    serializer_class= CustomerSerializer
    @csrf_exempt
    def post(self, request):
        try:
            password = request.POST.get('password')
        
            exist_customer=Customer.objects.filter(customer__email=request.POST.get('email'))
            if not exist_customer.exists():
                customer=stripe.Customer.create(email=request.POST.get('email'),name=request.POST.get('name'),address={
                    "line1": request.POST.get('address'),
        "postal_code": request.POST.get('address'),
        "city": request.POST.get('address'),
        "state": request.POST.get('address'),
        "country": "US",
                })
                # stripe_source = stripe.Customer.create_source(customer.stripe_id, source="tok_in")
                Customer.objects.create(customer=User.objects.create(email=request.POST.get('email'),username=request.POST.get('username'),password=make_password(password)),stripe_id=customer.id,address=request.POST.get('address'))
                return JsonResponse({"customer":"created"})
            else:
                return JsonResponse({"customer":"exists"})
        except:
            return Response("pasword should not be null please enter a password to register")
                       
class PlanApiView(ListAPIView):
    queryset =Plan.objects.all()
    serializer_class= PlanSerializer
    @csrf_exempt
    def post(self, request):
        exist_plan=Plan.objects.filter(Name=request.POST.get('plan'))
        if not exist_plan.exists():
            plan=stripe.Product.create(name=request.POST.get('plan'),description=request.POST.get('description'),images=request.POST.get('images'))
            price=stripe.Price.create(active=True,
  unit_amount=int(request.POST.get('price'))*100,
  currency="inr",
  recurring={"interval": "month"},
  product=plan.id,
)
            Plan.objects.create(Name=plan.name,plan_id=plan.id,Price=price.unit_amount,Description=request.POST.get('description'),Image=request.POST.get('images'),stripe_price_id=price.id)
            return JsonResponse({"Plan":"created"})
        else:
            return JsonResponse({"Plan":"exists"})
    pass

class CustomerLogin(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            password=request.POST.get('password')
            customer=Customer.objects.get(customer__email=request.POST.get('email'))
            if check_password(password,customer.customer.password):
                payload={
                        'id':customer.id,
                        "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=20),
                        'iat': datetime.datetime.utcnow(),
                    }
                token=jwt.encode(payload,'secrate',algorithm='HS256')
                response = Response()
                response.set_cookie(key='jwt',value=token)
                response.data ={
                        'jwt':token
                }
                return response
            else:
                return Response("Password incorrect  please try again")
        except:
            return JsonResponse({'customer':'does not exists login again'})

class PlanPurchaseView(ListAPIView):
    queryset =Customer.objects.all().exclude(stripe_subscription_id=None)
    serializer_class= CustomerSerializer
    @csrf_exempt
    def post(self, request):
        if jwt_authentication(request) == None:
            return JsonResponse({'authentication-error':"You have no tocken or your token is expired so that you can not buy any planes: please login first to generate token then continue your shopping"})
        else:
            customer=Customer.objects.get(id=jwt_authentication(request)['id'])
            try:
                if customer.plan != None or customer.has_active_plan == True:
                    return Response("You are already subscriber for a plan")
                plan = Plan.objects.get(Name=request.data["plan"])
                stripe_source = stripe.Customer.create_source(customer.stripe_id, source="tok_in")
                customer.payment_method=stripe_source.id
                stripe_subscription = stripe.Subscription.create(customer=customer.stripe_id, default_source=customer.payment_method, items=[{"price":plan.stripe_price_id}])
                customer.stripe_subscription_id=stripe_subscription.id
                customer.plan=plan
                customer.has_active_plan =True
                
                customer.save()
            except:
                return Response("Product the you've selected doesnot exists")
            invoice = stripe.Invoice.retrieve(stripe_subscription.latest_invoice)
            payment_intent = stripe.PaymentIntent.retrieve(invoice.payment_intent)
            url = payment_intent.next_action.use_stripe_sdk.stripe_js
            webbrowser.open(url, new=0, autoraise=True)
            return Response(f"Subscription purchased successfully.......😍🤑 please check your browser to authenticate if not opened then please hit this url {url}")


class FacebookLoginView(ListAPIView):
    @csrf_exempt
    def post(self, request):
        token = request.data['token']
        req1 = requests.get(f"https://graph.facebook.com/v13.0/me?fields=id%2Cname%2Cemail&access_token={token}")
        data = req1.json()
        return Response(data)
    



class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2AdapterIdToken
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer
    callback_url = "http://localhost:8000/api/v1/users/login/google/callback/"

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
