"""
Helpers for colaraz API.
"""
import logging

from django.conf import settings
from django.contrib.sites.models import Site

from oscar.core.loading import get_model

from ecommerce.core.models import SiteConfiguration
from ecommerce.theming.models import SiteTheme

LOGGER = logging.getLogger(__name__)
Partner = get_model('partner', 'Partner')


def get_or_create_site(site_url):
    """
    Get or create site
    """
    site, _ = Site.objects.get_or_create(
        domain=site_url,
        defaults={'name': site_url}
    )
    LOGGER.info('Site with domain ({}) {}'.format(
            site_url,
            'already exists.' if _ else 'is created.'
        )
    )
    return site


def get_partner(site_partner):
    """
    Returns Partner having specific short_code
    """
    return Partner.objects.filter(
        short_code=site_partner
    ).first()


def create_site_theme(site, theme):
    """
    Map site with site-theme
    """
    if settings.DEFAULT_SITE_THEME != theme:
        SiteTheme.objects.update_or_create(
            site=site,
            defaults={
                'theme_dir_name': theme
            }
        )
        LOGGER.info('Site ({}) is mapped with theme ({})'.format(site, theme))


def create_site_configurations(
    site,
    partner,
    lms_site_url,
    payment_processors,
    client_side_payment_processor,
    payment_support_email,
    from_email,
    oauth_settings
):
    """
    Create Site-Configurations with provided data
    """
    site_data = {
        'partner': partner,
        'lms_url_root': lms_site_url,
        'payment_processors': payment_processors,
        'client_side_payment_processor': client_side_payment_processor,
        'from_email': from_email or getattr(settings, 'OSCAR_FROM_EMAIL', ''),
        'payment_support_email': payment_support_email or
        getattr(settings, 'DEFAULT_PAYMENT_SUPPORT_EMAIL', ''),
        'discovery_api_url': getattr(settings, 'DISCOVERY_API_URL_ROOT', ''),
        'oauth_settings': oauth_settings,
    }
    SiteConfiguration.objects.update_or_create(
        site=site,
        defaults=site_data,
    )
    LOGGER.info('Site {} is mapped with following configurations {}'.format(site, site_data))
