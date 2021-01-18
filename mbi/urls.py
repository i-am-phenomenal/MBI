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
from backend.Views.manager_view import ManagerView, ManagerListCreateView, ManagerRetreiveDestroyView
from backend.Views.product_view import ProductView, ProductListCreateView, ProductRetreiveDestroyView
from backend.Views.price_view import PriceView, PriceListCreateView, PriceRetreiveDestroyView
from backend.Views.subscription_view import SubscriptionView
from backend.Views.payment_method_view import PaymentMethodView, PaymentListCreateView, PaymentRetreiveDestroyView

managerView = ManagerView()
productView = ProductView()
priceView = PriceView()
subsView = SubscriptionView()
paymentView = PaymentMethodView()

urlpatterns = [
    path('admin/', admin.site.urls),

    path("manager/signup/", managerView.signUp),
    path("manager/login/", managerView.login),
    path("manager/update_payment_method/", managerView.updatePaymentMethod),
    path("manager/remove_card_details/", managerView.removePaymentMethod),
    path("manager/get_payment_methods/<str:managerId>", managerView.getAllPaymentMethods),
    path("manager/add_default_payment/", managerView.addDefaultPaymentMethod),
    path("manager/get_details/", managerView.getManagerDetailsByToken),
    path("manager/", ManagerListCreateView.as_view()),
    path("manager/<str:id>/", ManagerRetreiveDestroyView.as_view()),

    path("product/", ProductListCreateView.as_view()),
    path("product/<str:id>/", ProductRetreiveDestroyView.as_view()),
    # path("product/create/", productView.createProduct),

    path("price/", PriceListCreateView.as_view()),
    path("price/<str:id>", PriceRetreiveDestroyView.as_view()),
    path("price/create/", priceView.createPrice),
    path("price/get_all/", priceView.getAllPrices),
    path("price/delete/", priceView.deletePriceById),

    path("payment_method/", PaymentListCreateView.as_view()),
    path("payment_method/<str:id>/", PaymentRetreiveDestroyView.as_view()),
    path("payment_method/create/", paymentView.createPaymentMethod),
    path("payment_method/get_card_details/<str:managerId>/", paymentView.getCardDetails),
    path("payment_method/setup_intent/", paymentView.setupPaymentIntent),
    path("payment_method/payment_intent/", paymentView.createPaymentIntent),

    path("subscriptions/create/", subsView.createSubscription),
    path("subscriptions/get_available/<str:managerId>/", subsView.getAvailableSubscriptionsAndPrice),
    path("subscriptions/delete/", subsView.removeSubscription)

]
