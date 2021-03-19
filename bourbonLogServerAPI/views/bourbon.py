"""View module for handling requests about logs"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from bourbonLogServerAPI.models import Log, Logger


class LogView(ViewSet):
    """Bourbon Log Logs"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized log instance
        """

        # Uses the token passed in the `Authorization` header
        logger = Logger.objects.get(user=request.auth.user) 

        # Create a new Python instance of the Log class
        # and set its properties from what was sent in the
        # body of the request from the client.
        log = Log()
        
        log.bourbon_name = request.data["bourbonName"]
        log.distiller = request.data["distiller"]
        log.proof = request.data["proof"]
        log.price = request.data["price"]
        log.age = request.data["age"]
        log.batch_num = request.data["batchNum"]
        log.rating = request.data["rating"]
        log.notes = request.data["notes"]
        # log.post_image_url = request.data["postImageUrl"]
        log.logger = logger

        # Try to save the new log to the database, then
        # serialize the log instance as JSON, and send the
        # JSON as a response to the client request
        try:
            log.save()
            serializer = LogSerializer(log, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single log

        Returns:
            Response -- JSON serialized log instance
        """

        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/logs/2
            #
            # The `2` at the end of the route becomes `pk`
            log = Log.objects.get(pk=pk)
            
            serializer = LogSerializer(log, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Handle PUT requests for a log

        Returns:
            Response -- Empty body with 204 status code
        """
        logger = Logger.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Log, get the log record
        # from the database whose primary key is `pk`
        log = Log.objects.get(pk=pk)
        log.bourbon_name = request.data["bourbonName"]
        log.distiller = request.data["distiller"]
        log.proof = request.data["proof"]
        log.price = request.data["price"]
        log.age = request.data["age"]
        log.batch_num = request.data["batchNum"]
        log.rating = request.data["rating"]
        log.notes = request.data["notes"]
        # log.post_image_url = request.data["postImageUrl"]
        log.logger = logger

        log.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single log

        Returns:
            Response -- 200, 404, or 500 status code
        """

        try:
            log = Log.objects.get(pk=pk)
            log.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Log.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to logs resource

        Returns:
            Response -- JSON serialized list of logs
        """
        #get all logs for a single logger. Gets all logs, but does it according to the user and 
        #is set to the user_id value found in the model


        logs = Log.objects.filter(logger__user=request.auth.user)


        serializer = LogSerializer(
            logs, many=True, context={'request': request})
        return Response(serializer.data)

class LogSerializer(serializers.ModelSerializer):
    """JSON serializer for logs

    Arguments:
        serializer type
    """
    class Meta:
        model = Log
        fields = ('id', 'logger', 'bourbon_name','distiller', 'proof', 'price',
        'age', 'batch_num', 'notes','rating'
        )
        depth = 1