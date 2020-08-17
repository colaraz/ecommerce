"""
Views for colaraz API.
"""
import logging

from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers as rest_serializers

from ecommerce.colaraz_features.api import serializers
from ecommerce.extensions.api.permissions import IsStaffOrOwner

LOGGER = logging.getLogger(__name__)


class SiteOrgViewSet(viewsets.ViewSet):
    """
    View set to enable creation of site, organization and theme via REST API.
    """
    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthenticated, IsStaffOrOwner,)
    serializer_class = serializers.SiteOrgSerializer

    def create(self, request):
        """
        Perform creation operation for site, organization, site theme and site configuration.
        """
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.create(serializer.validated_data)
                LOGGER.info('Site is successfully created on ecommerce')
        except (rest_serializers.ValidationError, ValueError, NameError) as ex:
            return Response(
                {'error': str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except:
            return Response(
                {'error': 'Request data is unappropriate'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'success': serializer.validated_data},
            status=status.HTTP_201_CREATED
        )
