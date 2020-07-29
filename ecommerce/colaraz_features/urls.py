from django.conf.urls import url, include

from ecommerce.colaraz_features import views
from ecommerce.colaraz_features.api import urls

app_name = 'colaraz_features'

urlpatterns = [
    url(r'^api/v1/', include(urls.urlpatterns, namespace='colaraz_api')),
]
