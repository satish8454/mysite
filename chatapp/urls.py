from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/",views.login_view,name="login"),
    path("signup/",views.signup_view,name="signup"),
    path("logout/",views.logout_view,name='logout'),
    path("chats/",views.chat_view,name='chats'),
    path("fetch_messages/<int:user_id>/", views.fetch_messages, name="fetch_messages"),
    path("send_message/", views.send_message, name="send_message"),
]