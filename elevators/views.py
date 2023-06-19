from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Elevator, UserRequest
from .serializers import ElevatorSerializer, UserRequestSerializer
from django.db.models import Max


class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    @action(detail=False, methods=['post'])
    def create_elevator(self, request):
        # Retrieve the highest elevator number
        highest_number = Elevator.objects.aggregate(Max('elevator_number'))[
            'elevator_number__max']

        # If there are existing elevators, increment the highest number by 1
        if highest_number is not None:
            elevator_number = highest_number + 1
        else:
            elevator_number = 1
        elevator_data = {
            'elevator_number': elevator_number,
            'status': 'idle',
            'current_floor': 0,
            'destination_floor': None
        }
        serializer = self.get_serializer(data=elevator_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
    
    # @action(detail=False, methods=['post'])
    # def create_elevator(self, request):
    #     elevator_data = {
    #         'elevator_number': 1,
    #         'status': 'idle',
    #         'current_floor': 0,
    #         'destination_floor': None
    #     }
    #     serializer = self.get_serializer(data=elevator_data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=201)

    @action(detail=True, methods=['get'])
    def requests(self, request, pk=None):
        elevator = self.get_object()
        requests = UserRequest.objects.filter(elevator=elevator)
        serializer = UserRequestSerializer(requests, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def next_destination(self, request, pk=None):
        elevator = self.get_object()
        requests = UserRequest.objects.filter(elevator=elevator)
        if not requests.exists():
            return Response({'message': 'No pending requests for this elevator.'}, status=404)
        destination_floor = requests.first().floor_number
        return Response({'next_destination': destination_floor})

    @action(detail=True, methods=['get'])
    def moving_direction(self, request, pk=None):
        elevator = self.get_object()
        if elevator.status != 'running':
            return Response({'message': 'The elevator is not currently running.'}, status=404)
        if elevator.destination_floor > elevator.current_floor:
            direction = 'up'
        else:
            direction = 'down'
        return Response({'moving_direction': direction})


class UserRequestViewSet(viewsets.ModelViewSet):
    queryset = UserRequest.objects.all()
    serializer_class = UserRequestSerializer

    def create(self, request, *args, **kwargs):
        elevator_id = request.data.get('elevator')
        if not elevator_id:
            return Response({'message': 'Please provide the elevator ID.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            elevator = Elevator.objects.get(id=elevator_id)
        except Elevator.DoesNotExist:
            return Response({'message': 'Invalid elevator ID.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(elevator=elevator)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def index(request):
    return render(request, 'index.html')
