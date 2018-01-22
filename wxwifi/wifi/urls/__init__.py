from django.conf.urls import url, include
from django.views.decorators.cache import cache_control

from wechat.urls import public as public_urls
from wechat.urls import pay as pay_urls
from wechat.urls import chat_room as chat_room_urls
from wechat.urls import component as component_urls
from wechat.urls import robot as robot_urls
from wechat.urls import wifi as wifi_urls
from wechat.views import public, pay, component, chat_room

urlpatterns = [
    url(r'public/', include(public_urls)),
    url(r'pay/', include(pay_urls)),
    url(r'chat_room/', include(chat_room_urls)),
    url(r'component/', include(component_urls)),
    url(r'robot/', include(robot_urls)),
    url(r'wifi/', include(wifi_urls)),
]
