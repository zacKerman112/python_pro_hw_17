from my.views import test_orm_view
from django.urls import path

urlpatterns = [
    path('main/', test_orm_view, name='test'),
]