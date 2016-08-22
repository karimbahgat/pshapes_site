"""pshapes_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib.gis import admin

admin.site.site_header = "Pshapes Website Admin"

urlpatterns = [

    # -----
    # HOME
    url('^$', "pshapes_site.views.home"),


    # ------------
    # INTERACTIVE
    url('^interactive/$', "provshapes.views.interactive"),


    # -----------
    # CONTRIBUTE
    url('^contribute/$', "provchanges.views.contribute"),

    # country
    url('^contribute/view/(?P<country>[a-zA-Z0-9\-\_]*)/$', "provchanges.views.viewcountry"),
    url('^contribute/add/$', "provchanges.views.addcountry"),
    url('^contribute/edit/(?P<country>[a-zA-Z0-9\-\_]*)/$', "provchanges.views.editcountry"),

    # province (event or change depending on get params)
    url('^contribute/view/(?P<country>[a-zA-Z0-9\-\_]*)/(?P<province>[a-zA-Z0-9\-\_]*)/$', "provchanges.views.viewprov"), # event
    url('^contribute/add/(?P<country>[a-zA-Z0-9\-\_]*)/$', "provchanges.views.addprov"),
    url('^contribute/add/(?P<country>[a-zA-Z0-9\-\_]*)/(?P<province>[a-zA-Z0-9\-\_]*)/$', "provchanges.views.addprov"),
    url('^contribute/edit/(?P<country>[a-zA-Z0-9\-\_]*)/(?P<province>[a-zA-Z0-9\-\_]*)/$', "provchanges.views.editprov"), # event

    # provchange (should be phased out, maybe allow via get param instead?)
    url(r'^provchange/(?P<pk>[0-9]+)/edit/$', "provchanges.views.editchange", name="editchange"),
    url(r'^provchange/(?P<pk>[0-9]+)/view/$', "provchanges.views.viewchange", name="viewchange"),


    # ------
    # ABOUT
    url('^about/$', "pshapes_site.views.about"),


    # -----
    # DATA
    url('^data/$', "provshapes.views.data"),



    # --------
    # (USERS)
    url('^registration/$', "provchanges.views.registration"),
    url('^login/$', "provchanges.views.login"),
    url('^logout/$', "provchanges.views.logout"),


    # -------
    # (TESTING)
    url('^testgrid/$', "pshapes_site.views.testgrid"),
    url('^timetest/$', "cshapes.views.mapview"),
    url(r'^admin/$', include(admin.site.urls)),


    
]

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns.extend([
                    url(r'^api/cshapes/$', "cshapes.views.apiview")
                    ])
