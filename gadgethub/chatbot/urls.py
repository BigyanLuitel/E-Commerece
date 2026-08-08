from django.urls import path
from . import views

app_name = "chatbot"

urlpatterns = [
    path("send/", views.chat_send, name="send"),
    path("reset/", views.chat_reset, name="reset"),
    path("history/", views.chat_history, name="history"),
]