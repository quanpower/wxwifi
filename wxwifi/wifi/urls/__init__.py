from django.conf.urls import url, include
from django.views.decorators.cache import cache_control


from wifi.urls import wifi as wifi_urls

urlpatterns = [

    url(r'wifi/', include(wifi_urls)),
]
