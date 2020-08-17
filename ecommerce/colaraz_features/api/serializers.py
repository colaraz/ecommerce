"""
Serializers for colaraz API.
"""
from django.conf import settings

from oscar.core.loading import get_model
from rest_framework import serializers

from ecommerce.colaraz_features.api.helpers import (
    create_site_configurations,
    create_site_theme,
    get_or_create_site,
    get_partner,
)


Partner = get_model('partner', 'Partner')
DEFAULT_FROM_EMAIL = getattr(settings, 'OSCAR_FROM_EMAIL', '')
DEFAULT_SUPPORT_EMAIL = getattr(settings, 'DEFAULT_PAYMENT_SUPPORT_EMAIL', '')


class SiteOrgSerializer(serializers.Serializer):
    lms_site_url = serializers.URLField(required=True)
    ecommerce_site_domain = serializers.CharField(max_length=90, required=True)
    site_theme = serializers.CharField(max_length=255, required=False, default=settings.DEFAULT_SITE_THEME)
    site_partner = serializers.CharField(max_length=255, required=False, default='edx')
    payment_processors = serializers.CharField(max_length=255, required=False, default='')
    client_side_payment_processor = serializers.CharField(max_length=255, required=False, default='')
    ecommerce_from_email = serializers.EmailField(max_length=255, required=False, allow_blank=True, default=DEFAULT_FROM_EMAIL)
    payment_support_email = serializers.EmailField(max_length=255, required=False, allow_blank=True, default=DEFAULT_SUPPORT_EMAIL)
    oauth_settings = serializers.JSONField(required=True)

    @staticmethod
    def validate_site_partner(value):
        """
        Validate site partner.
        """
        if not Partner.objects.filter(short_code=value).exists():
            raise serializers.ValidationError('A Partner with short_code "{}" does not exists.'.format(value))
        return value

    def create(self, validated_data):
        """
        Create instances of site, site theme and site configuration on ecommerce.
        """
        site = get_or_create_site(validated_data['ecommerce_site_domain'])
        create_site_theme(site, validated_data['site_theme'])
        create_site_configurations(
            client_side_payment_processor=validated_data['client_side_payment_processor'],
            from_email=validated_data['ecommerce_from_email'],
            lms_site_url=validated_data['lms_site_url'],
            oauth_settings=validated_data['oauth_settings'],
            partner=get_partner(validated_data['site_partner']),
            payment_processors=validated_data['payment_processors'],
            payment_support_email=validated_data['payment_support_email'],
            site=site,
        )
