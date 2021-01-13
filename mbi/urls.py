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
from backend.Views.manager_view import ManagerView
from backend.Views.product_view import ProductView
from backend.Views.price_view import PriceView
from backend.Views.subscription_view import SubscriptionView

managerView = ManagerView()
productView = ProductView()
priceView = PriceView()
subsView = SubscriptionView()

urlpatterns = [
    path('admin/', admin.site.urls),

    path("manager/signup/", managerView.signUp),
    path("manager/login/", managerView.login),

    path("product/create/", productView.createProduct),

    path("price/create/", priceView.createPrice),
    path("price/get_all/", priceView.getAllPrices),
    path("price/delete/", priceView.deletePriceById),

    path("subscriptions/create/", subsView.createSubscription)
]
