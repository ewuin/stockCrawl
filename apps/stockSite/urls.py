from django.conf.urls import url, static
from . import views           # This line is new!
from django.conf import settings
from .models import all_stock_names
#from django.views.generic import TemplateView


urlpatterns = [
    #url(r'^index$', views.index),
    url(r'^crawlbb$', views.crawlbb),
    url(r'^crawlcnbc$', views.crawlcnbc),
    url(r'^$', views.landing,name="home"),
    url(r'^search/$',views.stockSearchAutocomplete.as_view(model=all_stock_names)
            ,name='search'), # responds to format http://localhost:5000/search/?q=apple
    url(r'^customText$', views.customText),
    ]

# This is required for static files while in development mode. (DEBUG=TRUE)
# No, not relevant to scrapy or crawling :)
#if settings.DEBUG:
#    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
