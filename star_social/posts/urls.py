from django.urls import path, re_path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostList.as_view(), name='all'),
    path('new/', views.CreatePost.as_view(), name='create'),
    re_path(r'^by/(?P<username>[-\w]+)/$', views.UserPosts.as_view(), name='for_user'),
    re_path(r"^by/(?P<username>[-\w]+)/(?P<pk>[\d]+)/$", views.PostDetail.as_view(), name='single'),
    re_path(r"^update/(?P<pk>[\d]+)/$", views.UpdatePost.as_view(), name='post_update'),
    re_path(r"^delete/(?P<pk>[\d]+)/$", views.DeletePost.as_view(), name='delete'),
    # comments
    re_path(r"^(?P<pk>[\d]+)/comment/$", views.add_commment, name='comment'),
    re_path(r"^comment/(?P<pk>[\d]+)/remove/$", views.delete_comment, name='remove_comment'),
]