""""
Landing Urls, Simple
"""

from django.urls import path
from .views import LandingView, ProductsView, AboutusView

urlpatterns = [
    path("", LandingView.as_view(), name='home'),
    path("about-us", AboutusView.as_view(), name='about-us'),
    path("products", ProductsView.as_view(), name='products'),

]