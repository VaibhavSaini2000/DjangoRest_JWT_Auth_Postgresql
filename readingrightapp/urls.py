from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('posts',views.PostView)

urlpatterns = [
    path('',include(router.urls)),
    path('demo',views.DemoView.as_view()),
    path('postsjson/',views.PostjsonView.as_view())
]