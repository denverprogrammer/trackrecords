### urls.py
from django.urls import include, path

from . import views

app_name = 'membership'
urlpatterns = [
       path('memberships/', views.MembershipView.as_view(), name='select'),
]