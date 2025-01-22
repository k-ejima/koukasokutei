from django.urls import path
from . import views

app_name = 'Ejinews'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('news-detail/<int:pk>', views.NewsDetail.as_view(), name='news_detail'),
    path('news-detail/<int:news_id>/add-comment/', views.add_comment, name='add_comment'),
    path('government-list/', views.GovernmentView.as_view(), name='government_list'),
    path('entertainment-list/', views.EntertainmentView.as_view(), name='entertainment_list'),
    path('sports-list/', views.SportsView.as_view(), name='sports_list'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('search/', views.search, name='search'),
]