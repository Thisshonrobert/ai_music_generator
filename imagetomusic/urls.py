from django.urls import path
from . import views
from .views import ProcessImageView

urlpatterns = [
    path('',views.home,name="home"),
    path('process-image/', ProcessImageView.as_view(), name='process-image')
]