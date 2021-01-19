"""mbi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend.Views.manager_view import ManagerView, ManagerRemoveCardDetailsView, ManagerListCreateView, ManagerRetreiveDestroyView, ManagerUpdateView, ManagerRetreivePaymentMethod
from backend.Views.product_view import  ProductListCreateView, ProductRetreiveDestroyView
from backend.Views.price_view import  PriceListCreateView, PriceRetreiveDestroyView
from backend.Views.subscription_view import  SubscriptionListCreateView, SubscriptionRetreiveDestroyView, SubscriptionListAPIView
from backend.Views.payment_method_view import  PaymentListCreateView, PaymentRetreiveDestroyView, PaymentIntentCreateView, SetupPaymentIntentView

managerView = ManagerView()

urlpatterns = [
    path('admin/', admin.site.urls),

    path("manager/signup/", managerView.signUp),
    path("manager/", ManagerListCreateView.as_view()),
    path("manager_login/", managerView.login),
    path("manager/update_payment_method/", ManagerUpdateView.as_view()),
    path("manager/remove_card_details/<str:paymentMethodId>/", ManagerRemoveCardDetailsView.as_view()),
    path("manager/get_payment_method/<str:id>/", ManagerRetreivePaymentMethod.as_view()),
    path("get_manager_details/", managerView.getManagerDetailsByToken),

    path("product/", ProductListCreateView.as_view()),
    path("product/<str:id>/", ProductRetreiveDestroyView.as_view()),

    path("price/", PriceListCreateView.as_view()),
    path("price/<str:id>", PriceRetreiveDestroyView.as_view()),

    path("payment_method/", PaymentListCreateView.as_view()),
    path("payment_method/<str:id>/", PaymentRetreiveDestroyView.as_view()),
    path("setup_intent/", SetupPaymentIntentView.as_view()),
    path("payment_intent/", PaymentIntentCreateView.as_view()),

    path("subscriptions/", SubscriptionListCreateView.as_view()),
    path("subscriptions/get_all/<str:customer_id>/", SubscriptionListAPIView.as_view()),
    path("subscriptions/<str:id>/", SubscriptionRetreiveDestroyView.as_view()),
    path("subscriptions/create/", SubscriptionListCreateView.as_view()),
    path("subscriptions/delete/<str:id>/", SubscriptionRetreiveDestroyView.as_view())

]
