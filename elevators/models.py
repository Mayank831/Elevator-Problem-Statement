from django.db import models

class Elevator(models.Model):
    elevator_number = models.IntegerField(unique=True)
    status = models.CharField(max_length=12, choices=[('idle', 'Idle'), ('running', 'Running'), ('maintenance', 'Maintenance')])
    current_floor = models.IntegerField(default=0)
    destination_floor = models.IntegerField(null=True)

    def __str__(self):
        return f"Elevator {self.elevator_number}"


class UserRequest(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    floor_number = models.IntegerField()
    direction = models.CharField(max_length=5, choices=[('up', 'Up'), ('down', 'Down')])

    def __str__(self):
        return f"User Request at floor {self.floor_number}"
