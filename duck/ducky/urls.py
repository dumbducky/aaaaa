from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("administration", views.administration, name='administration'),
    path("automod", views.automod, name='automod'),
    path("bot", views.bot, name='bot'),
    path("conversion", views.conversion, name='conversion'),
    path("files", views.files, name='files'),
    path("info", views.info, name='info'),    
    path("logging", views.logging, name='logging'),
    path("moderation", views.moderation, name='moderation'),
    path("roles", views.roles, name='roles'),
    path("server", views.server, name='server'),
    path("stats", views.stats, name='stats'),
    path("time", views.time, name='time'),
    path("tracking", views.tracking, name='tracking'),
    path("users", views.users, name='users'),
    path("utils", views.utils, name='utils'),
    path("warn", views.warn, name='warn'),
    path("config", views.config, name='config'),
    path("api_logging", views.api_logging, name='api_logging'),
    path("api_cookie", views.api_cookie, name='api_cookie'),
    path("server_select", views.server_select, name='server_select'),
    path("testing", views.testing, name='testing'),
    path("log_out", views.log_out, name='log_out')
]