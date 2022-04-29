from asyncio.windows_events import NULL
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

def jwt_authentication(request):
    try:
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        payload=jwt.decode(jwt_token,'secrate',algorithms=['HS256'])
        print("3945849805389534890",payload)
        return payload
    except:
        return None


class CustomerApiView(ListAPIView):
    queryset =Customer.objects.all()
    serializer_class= CustomerSerializer
    @csrf_exempt
    def post(self, request):
        exist_customer=Customer.objects.filter(customer__email=request.POST.get('email'))
        if not exist_customer.exists():
            customer=stripe.Customer.create(email=request.POST.get('email'),name=request.POST.get('name'))
            stripe_source = stripe.Customer.create_source(customer.stripe_id, source="tok_in")
            Customer.objects.create(customer=User.objects.create(email=request.POST.get('email'),username=request.POST.get('username')),stripe_id=customer.id,payment_method=stripe_source.id)
            return JsonResponse({"customer":"created"})
        else:
            return JsonResponse({"customer":"exists"})
                       
class PlanApiView(ListAPIView):
    queryset =Plan.objects.all()
    serializer_class= PlanSerializer
    @csrf_exempt
    def post(self, request):
        exist_plan=Plan.objects.filter(Name=request.POST.get('Name'))
        if not exist_plan.exists():
            plan=stripe.Product.create(name=request.POST.get('Name'),description=request.POST.get('description'),images=request.POST.get('images'))
            price=stripe.Price.create(
  unit_amount=request.POST.get('price'),
  currency="usd",
  recurring={"interval": "month"},
  product=plan.id,
)

            Plan.objects.create(Name=plan.name,plan_id=plan.id,Price=price.unit_amount,Description=request.POST.get('description'),Image=request.POST.get('images'),stripe_price_id=price.id)
            return JsonResponse({"Plan":"created"})
        else:
            return JsonResponse({"Plan":"exists"})
    pass

class PurchasePlan(ListAPIView):
    # plan=stripe.Plan.retrieve()
    pass
class CustomerLogin(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            customer=Customer.objects.get(customer__email=request.POST.get('email'))
            print(customer.id,"************************")
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
                if customer.wallet_balance ==0:
                    return Response("You have insufficient balance please top-up your wallet")
                plan = Plan.objects.get(Name=request.data["plan"])
                if float(request.data["price"]) != plan.Price:
                    return Response("You have entered wrong amount for the plan please enter again the actual price")

                print("&*&*&*&*&**")
                stripe_subscription = stripe.Subscription.create(customer=customer.stripe_id, default_source=customer.payment_method, items=[{"price":plan.stripe_price_id}])
                customer.stripe_subscription_id=stripe_subscription.id
                customer.plan=plan
                customer.has_active_plan =True
                customer.save()
            except:
                return Response("Product the you've selected doesnot exists")
            invoice = stripe.Invoice.retrieve(stripe_subscription.latest_invoice)
            payment_intent = stripe.PaymentIntent.retrieve(invoice.payment_intent)
            print(payment_intent,"******************************")
            return Response(f"Subscription purchased successfully.......😍🤑 varify your payment through below link: {payment_intent.next_action.use_stripe_sdk.stripe_js}")

