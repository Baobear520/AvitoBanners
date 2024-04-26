
from django.urls import path
from banners import views


urlpatterns = [
    #path('user-banner/',),
    path('banner/',views.banner_list),
    path('banner/<int:pk>',views.banner_detail)
]
