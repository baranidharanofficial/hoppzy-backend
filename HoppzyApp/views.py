from rest_framework import viewsets, status
from rest_framework.response import Response
from HoppzyApp.models import Bike
from HoppzyApp.serializers import BikeSerializer


class BikeViewSet(viewsets.ViewSet):
    queryset = Bike.objects.all()

    # Endpoint to get all bikes
    def list(self, request):
        bikes = Bike.objects.all()
        serializer = BikeSerializer(bikes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Endpoint to add a new bike
    def create(self, request):
        serializer = BikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This will call `create` method in BikeSerializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Optionally, you could add more actions, for example, to retrieve a single bike
    def retrieve(self, request, pk=None):
        try:
            bike = Bike.objects.get(pk=pk)
            serializer = BikeSerializer(bike)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Bike.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    # Optionally, you could add an action to update an existing bike
    def update(self, request, pk=None):
        try:
            bike = Bike.objects.get(pk=pk)
            serializer = BikeSerializer(bike, data=request.data)
            if serializer.is_valid():
                serializer.save()  # This will call `update` method in BikeSerializer
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Bike.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    # Optionally, you could add an action to delete a bike
    def destroy(self, request, pk=None):
        try:
            bike = Bike.objects.get(pk=pk)
            bike.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Bike.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
