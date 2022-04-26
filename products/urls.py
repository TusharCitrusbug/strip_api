from django.urls import path
from products.views import *

urlpatterns = [
    # path('CheckOutSessionView/', CheckOutSessionView.as_view(),name='CheckOutSessionView'),
    # path('check-out/', checkout.as_view(),name='checkout'),
    path('create-customer/', CustomerApiView.as_view(),name='CustomerApiView'),

]
