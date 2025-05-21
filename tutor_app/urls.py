from django.urls import path
from .views import diary_view, get_lessons

urlpatterns = [
    path('', diary_view, name='diary'),
    path('get_lessons/', get_lessons, name='get_lessons'),
]