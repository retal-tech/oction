""""
Landing Urls, Simple
"""

from django.urls import path
from .views import LandingView

urlpatterns = [
    path("", LandingView.as_view(), name='home'),
    path("about-us", LandingView.as_view(), name='about-us'),
    path("products", LandingView.as_view(), name='products'),

]