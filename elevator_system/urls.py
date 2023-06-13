from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from elevators.views import ElevatorViewSet, UserRequestViewSet

router = routers.DefaultRouter()
router.register(r'elevators', ElevatorViewSet)
router.register(r'user-requests', UserRequestViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('elevators.urls')),  
    # Add this line to include your app-specific URLs
     path('elevators/create/', ElevatorViewSet.as_view({'post': 'create_elevator'}), name='create_elevator'),
]
