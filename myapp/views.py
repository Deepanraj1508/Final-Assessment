from rest_framework import viewsets
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from requests.exceptions import RequestException
from rest_framework import status
import requests
from requests.exceptions import RequestException, Timeout
import logging



class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_data = {
            "error": False,
            "message": "Ok",
            "result": AccountSerializer(instance).data,
            "statusCode": status.HTTP_201_CREATED
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

logger = logging.getLogger(__name__)

class IncomingDataView(APIView):
    def post(self, request, *args, **kwargs):
        # Ensure the data is in JSON format
        if not request.content_type == 'application/json':
            return Response({"message": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract the app secret token from the request data
        app_secret_token = request.data.get('app_secret_token')
        if not app_secret_token:
            return Response({"message": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Validate and find the account associated with the app secret token
            account = Account.objects.get(app_secret_token=app_secret_token)
        except Account.DoesNotExist:
            return Response({"message": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

        # Process the valid data and send it to the account's destinations
        data = request.data
        del data['app_secret_token']  # Remove the token from the data before forwarding

        success = True
        errors = []
        sent_destinations = []

        for destination in account.destinations.all():
            headers = destination.headers
            try:
                print(f"Sending data to: {destination.url}")
                response = requests.request(
                    method=destination.http_method,
                    url=destination.url,
                    json=data,
                    headers=headers
                )
                response.raise_for_status()  # Raises HTTPError for bad responses
                sent_destinations.append(destination.url)
            except RequestException as e:
                success = False
                errors.append(f"Failed to send data to {destination.url}: {str(e)}")
                logger.error(f"Failed to send data to {destination.url}: {e}")

        response_data = {
            "message": "Data received successfully" if success else "Failed to send data to some destinations",
            "sent_destinations": sent_destinations,
            "errors": errors if not success else []
        }

        return Response(response_data, status=status.HTTP_200_OK if success else status.HTTP_207_MULTI_STATUS)

    def get(self, request, *args, **kwargs):
        return Response({"message": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)