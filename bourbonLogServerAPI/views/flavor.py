"""View module for handling requests about logs"""
# from django.core.exceptions import ValidationError
# from rest_framework import status
# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from bourbonLogServerAPI.models import Flavor


class FlavorView(ViewSet):
    """Bourbon Log Flavors"""

    def list(self, request):
        """Handle GET requests to logs resource

        Returns:
            Response -- JSON serialized list of logs
        """
        # Get all log records from the database
        flavor = Flavor.objects.all()


        serializer = FlavorSerializer(
            flavor, many=True, context={'request': request})
        return Response(serializer.data)

class FlavorSerializer(serializers.ModelSerializer):
    """JSON serializer for logs

    Arguments:
        serializer type
    """
    class Meta:
        model = Flavor
        fields = ('id', 'flavor')
        depth = 1