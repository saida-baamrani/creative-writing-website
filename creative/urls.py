
from django.urls import path

from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.LoginView,name='login'),
    path('registartion/', views.signup,name='register'),
    
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    path('profile/', views.update_profile,name='update'),
    path('story/', views.StoryCreate.as_view(),name='create'),
    path('story/(?P<pk>[0-9]+/add-chapter)', views.ChapterCreate.as_view(),name='add-chapter'),
    path('story/Mylist/', views.StoryUser.as_view(), name='story-user-list'),
    path('story/list/', views.StoryList.as_view(), name='story-list'),
    path('story/(?P<pk>[0-9]+/detail-story', views.story_detail, name='story-detail'),
    path('story/(?P<pk>[0-9]+/update-story)', views.story_update, name='story-update'),
    path('story/(?P<pk>[0-9]+/update-chapter)', views.ChapterUpdate.as_view(), name='update-chapter'),
    path('story/(?P<pk>[0-9]+/add-comment/', views.add_comment_to_post, name='add_comment'),
    path('story/(?P<pk>[0-9]+/read-chapter/', views.chapter_detail, name='chapter_detail'),
    path('logout/$', views.LogoutView,name='logout'),

]