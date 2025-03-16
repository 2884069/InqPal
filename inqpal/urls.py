from django.urls import path
from inqpal import views

app_name = 'inqpal'


urlpatterns = [
    path('', views.index, name='index'),#amber
    path('posts/trending/', views.trending, name='trending'),#nat
    path('posts/pals/', views.pals_posts, name='palsposts'),#nat
    path('posts/categories/', views.categories, name='categories'),#nat
    path('posts/categories/<str:category_name>/',views.show_category, name='show_category'),#nat
    path('account/signup/', views.signup, name='register'),#iryna
    path('account/login/', views.user_login, name='login'),#iryna
    path('logout/', views.user_logout, name='logout'),
    path('account/my_account/', views.my_account, name='my_account'),#wang
    path('account/my_account/make_post', views.make_post, name='make_post'),#amber
    path('account/my_account/edit_profile', views.edit_profile, name='edit_profile'),#wang
    path('account/my_account/add_pal', views.add_pal, name='add_pal'),#amber
]