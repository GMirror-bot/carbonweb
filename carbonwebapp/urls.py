from django.urls import path
from . import views
urlpatterns = [
    path('', views.login),
    path('login/', views.login),
    # path('main/', views.main),
    path('factor/', views.factor),
    path('distribute/', views.disrtribute),
    path('carbon/', views.carbon),
    path('strength/', views.strength),
    path('slump/', views.slump),
    path('register/', views.register),
    path('saveregister/', views.saveregister),

    # url(r'^$',views.index,name='index'),
    # path('play/playing/<int:song_id>/<str:category_id>/', views.playing),
    # path('playing/<int:song_id>/<str:category_id>/', views.playing),
    # path('singer/', views.singer_detail),
]