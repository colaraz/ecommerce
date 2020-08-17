"""
URL patterns for colaraz features application.
"""
from django.conf.urls import url
from ecommerce.colaraz_features.api.views import SiteOrgViewSet

urlpatterns = [
    url(r'^site-org/', SiteOrgViewSet.as_view({'post': 'create'}), name='site-org'),
]
