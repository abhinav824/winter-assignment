from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name='netsoc'

urlpatterns=[
            path('register/',views.new_user.create_user,name='createuser'),
            path('created/',views.new_user.user_created,name='registered'),
            path('home/',views.news_feed.home,name='home'),
            path('write/',views.news_feed.new_post,name='new_post'),
            path('',include('django.contrib.auth.urls')),
            path('<int:id>/save_comment/',views.datahandle.save_comment,name='save_comment'),
            path('<int:id>/delete_post/',views.datahandle.delete_post,name='delete_post'),
            path('<int:id>/delete_comment/',views.datahandle.delete_comment,name='delete_comment'),
            path('<int:id>/edit_post/',views.datahandle.edit_post,name='edit_post'),
            path('<int:id>/profile/',views.profile.profile_page,name='profile'),
            path('<int:id>/follow/',views.datahandle.followreq,name='follow'),
            path('<int:id>/unfollow/',views.datahandle.unfollow,name='unfollow'),
            path('<int:id>/subscribe/',views.datahandle.subsreq,name='subscribe'),
            path('<int:id>/unsubscribe/',views.datahandle.unsubsreq,name='unsubscribe'),
            path('user_list/',views.news_feed.user_list,name='user_list'),
            path('<int:id>/profile/followers/',views.profile.followers,name='followers'),
            path('<int:id>/profile/following/',views.profile.following,name='following'),
            path('<int:id>/profile/edit_profile/',views.datahandle.edit_profile,name='edit_profile'),
            path('<int:id>/profile/change_password/',views.datahandle.changepassword,name='change_password'),
            path('<int:id>/profile/description/',views.profile.describe,name='describe'),
            path('<int:id>/profile/UploadImage/',views.profile.UploadImage,name='UploadImage'),
            path('user_record/',views.datahandle.user_record,name='user_record'),
            path('auth',include('social_django.urls', namespace='social')),
            path('profile_completion/',views.datahandle.profile_completion,name='profile_completion'),

]
