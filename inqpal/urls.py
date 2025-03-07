from django.urls import path
from inqpal import views

app_name = 'inqpal'

#Testing the gitignore
urlpatterns = [
    path('', views.index, name='index'),#amber
    path('posts/trending/', views.trending, name='trending'),#nat
    path('posts/pals/', views.palsposts, name='palsposts'),#nat
    path('posts/categories/', views.categories, name='categories'),#nat
    path('posts/categories/<slug:category_name_slug>/',views.show_category, name='show_category'),#nat
    path('account/signup/', views.signup, name='signup'),#iryna
    path('account/login/', views.login, name='login'),#iryna
    path('account/my_account/', views.my_account, name='my_account'),#wang
    path('account/my_account/make_post', views.make_post, name='make_post'),#amber
    path('account/my_account/edit_profile', views.edit_profile, name='edit_profile'),#wang
    path('account/my_account/add_pal', views.add_pal, name='add_pal'),#amber
]