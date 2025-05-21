from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),
    path('gender/list', views.gender_list),
    path('gender/add', views.add_gender),
    path('gender/edit/<int:genderId>', views.edit_gender),
    path('gender/delete/<int:genderId>', views.delete_gender),
    path('user/list', views.user_list),
    path('user/add', views.add_user),
    path('user/edit/<int:userId>', views.edit_user),
    path('user/delete/<int:userId>', views.delete_user),
    path('user/changepass/<int:userId>', views.change_pass),
    path('login/', views.login_view),
    path('logout/', views.logout_view)
]