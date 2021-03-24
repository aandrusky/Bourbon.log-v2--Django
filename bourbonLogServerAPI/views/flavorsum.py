"""View module for handling requests about logs"""
from bourbonLogServerAPI.models.flavor import Flavor
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from bourbonLogServerAPI.models import FlavorSum, Log, Flavor


class FlavorSumView(ViewSet):
    """Handle GET requests to FlavorSum resource
    Returns:
        Response -- JSON serialized list of flavorsums
    """

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized flavorsum instance
        """

        # Create a new Python instance of the Log class
        # and set its properties from what was sent in the
        # body of the request from the client.

        flavor = Flavor.objects.get(pk=request.data["flavorId"])
        log = Log.objects.get(pk=request.data["logId"])

        try:

            found_flavorsum = FlavorSum.objects.get(flavor = flavor, log = log)

            found_flavorsum.delete()
                       
            flavorsum = FlavorSum()

            flavorsum.flavor_weight = request.data["flavorweight"]

            flavorsum.flavor = flavor

            flavorsum.log = log

        except ObjectDoesNotExist as ex:

            flavorsum = FlavorSum()

            flavorsum.flavor_weight = request.data["flavorweight"]

            flavorsum.flavor = flavor

            flavorsum.log = log


        # Try to save the new log to the database, then
        # serialize the log instance as JSON, and send the
        # JSON as a response to the client request
        try:
            flavorsum.save()
            serializer = FlavorSumSerializer(flavorsum, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)




    def list(self, request):

        # authenticated_user = Logger.objects.get(user=request.auth.user)

        
        #gets value of logId in qsp, stores in 'log' -- might need to parse into integer?
        log = (self.request.query_params.get('logId', None))    
        
        #if a log exists, 
        if log is not None:
            #get all flavors for a single log entry. Gets all flavorsums, but does it according to the number that was found above, and 
            #is set to the log_id value found in the model
            flavorsums = FlavorSum.objects.filter(log_id = int(log))

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

    
