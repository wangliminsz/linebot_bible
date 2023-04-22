"""b_bot URL Configuration

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
from django.urls import include, path

#-----------------2021-09-06

from django.views.static import serve
from b_bot.settings import MEDIA_ROOT
from b_bot.settings import STATIC_ROOT

from django.conf import settings
from django.conf.urls.static import static

#-----------------2021-09-06

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bbot_app.urls')),

    # path('media/(?P<path>.*)$',serve, {"document_root": MEDIA_ROOT}), #是 Django 2 版本，不行 
]

# if settings.DEBUG:
if True:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     
