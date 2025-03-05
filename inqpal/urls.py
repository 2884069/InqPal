from django.urls import path
from inqpal import views

app_name = 'inqpal'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/trending/', views.trending, name='trending'),
    path('posts/pals/', views.palsposts, name='palsposts'),
    path('posts/categories/', views.categories, name='categories'),
    path('posts/categories/<slug:category_name_slug>/',views.show_category, name='show_category'),
    path('account/signup/', views.signup, name='signup'),
    path('account/login/', views.login, name='login'),
    path('account/my_account/', views.my_account, name='my_account'),
    path('account/my_account/make_post', views.make_post, name='make_post'),
    path('account/my_account/edit_profile', views.edit_profile, name='edit_profile'),
    path('account/my_account/add_pal', views.add_pal, name='add_pal'),
]