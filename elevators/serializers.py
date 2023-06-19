from rest_framework import serializers
from .models import Elevator, UserRequest


class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = ['elevator_number', 'status',
                  'current_floor', 'destination_floor']


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = ['elevator', 'floor_number', 'direction']
