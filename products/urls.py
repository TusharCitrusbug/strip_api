from django.urls import path
from products.views import *

urlpatterns = [
    # path('CheckOutSessionView/', CheckOutSessionView.as_view(),name='CheckOutSessionView'),
    # path('check-out/', checkout.as_view(),name='checkout'),
    path('create-customer/', CustomerApiView.as_view(),name='CustomerApiView'),
    path('customer-list/', CustomerApiView.as_view(),name='CustomerApiView'),
    path('create-plan/', PlanApiView.as_view(),name='CustomerApiView'),
    path('plan-list/', PlanApiView.as_view(),name='CustomerApiView'),
    path('purchase-plan/', PlanPurchaseView.as_view(),name='PlanPurchaseView'),
    path('login/', CustomerLogin.as_view(),name='CustomerLogin'),
    path('purchase-plan/', PlanPurchaseView.as_view(),name='PlanPurchaseView'),
    path('api/facebook-login/', FacebookLoginView.as_view(),name='FacebookLoginView'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
   

    
]

