"""blog2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from main import urls as urlsMain
from django.conf import settings
from posts import urls as urlsPosts
from accounts import urls as accUrls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(urlsMain, namespace="main")),
    url(r'^posts/', include(urlsPosts, namespace="posts")),
    url(r'^accounts/', include(accUrls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(
    	regex=r'^media/(?P<path>.*)$',
    	view="django.views.static.serve",
    	kwargs={'document_root':settings.MEDIA_ROOT}
    	),
]
