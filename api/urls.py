from django.urls import path

from api.views import start_view

urlpatterns = [
    path('start/', start_view, name='start')
]
