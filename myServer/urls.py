"""myServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import view, initdb, act, adminDb

urlpatterns = [
    # url(r'^$', view.hello),
    url(r'^$', adminDb.hello),
    url(r'^initdb$', initdb.create),
    url(r'^admin/', admin.site.urls),

    url(r'^login$', act.login),
    url(r'^setPwd$', act.setPwd),
    url(r'^browse$', act.browse),
    url(r'^evaluate$', act.evaluate),
    url(r'favorite$', act.fav),
    url(r'^hot$', act.hot),
    url(r'^getComm$', act.getComm),
    url(r'^getMyFav$', act.getMyFav),
    url(r'^getMyComm$', act.getMyComm),
    url(r'^getATxt$', act.getATxt),
    url(r'^search$', act.search),
    url(r'^top10$', act.top10),

    # url(r'^adminDb$', adminDb.home),
    url(r'^home$', adminDb.home),
    url(r'^showTable$', adminDb.showTable),
    url(r'^addStBatch$', adminDb.addStBatch),
    url(r'^addCsBatch$', adminDb.addCsBatch),
    url(r'^addJnBatch$', adminDb.addJnBatch),
    url(r'^addLine$', adminDb.addLine),

    url(r'^delStLine$', adminDb.delStLine),
    url(r'^delCsLine$', adminDb.delCsLine),
    url(r'^delJnLine$', adminDb.delJnLine),
    url(r'^delCmLine$', adminDb.delCmLine),

]
urlpatterns += staticfiles_urlpatterns()
