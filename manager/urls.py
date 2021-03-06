"""manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from telegram_bot import views as tgviews
from . import config


urlpatterns = [
    path('admin/', admin.site.urls),
    path('anime/', tgviews.anime),
    path('telegram_bot/', tgviews.index),
    path('task_activity/', tgviews.mng),
    path('manager1c/', tgviews.msg),
    path('krasa_winner/', tgviews.Egor.index),
    path('guess/', tgviews.Egor.guess),
    path('passgen/', tgviews.Egor.passgen),
    path('chat', tgviews.chat),
    path('api/', include('telegram_bot.api.urls')),
    path(config.TG_API_KEY + '/', tgviews.tg),
    path('', tgviews.index, name="index"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
