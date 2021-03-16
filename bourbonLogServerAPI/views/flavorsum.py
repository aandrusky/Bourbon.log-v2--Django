"""View module for handling requests about logs"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from bourbonLogServerAPI.models import Log, Logger, FlavorSum


class FlavorSumView(ViewSet):
    """Handle GET requests to FlavorSum resource
    Returns:
        Response -- JSON serialized list of events
    """
    def list(self, request):

        # authenticated_user = Logger.objects.get(user=request.auth.user)

        
        #gets value of logId in qsp, stores in 'log' -- might need to parse into integer?
        log = float(self.request.query_params.get('logId', None))    #is log actually getting a number?

        #if a log exists, 
        if log is not None:
            #get all flavors for a single log entry. Gets all flavorsums, but does it according to the number that was found above, and 
            #is set to the log_id value found in the model
            flavorsums = FlavorSum.objects.filter(log_id = log)

        else:
            flavorsums = FlavorSum.objects.all()
                    


        serializer = FlavorSumSerializer(flavorsums, many=True, context={'request': request})

        return Response(serializer.data)
            



class FlavorSumSerializer(serializers.ModelSerializer):
    """JSON serializer for logs

    Arguments:
        serializer type
    """
    class Meta:
        model = FlavorSum
        fields = ('id', 'flavor_weight', 'flavor','log')
        depth = 1

    
