from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewset(viewsets.ModelViewSet):
  queryset = CustomUser.objects.all()
  serializer_class = CustomUserSerializer

  def get_permissions(self):
    if self.request.method == 'GET' or self.request.method == 'PUT':
      self.permission_classes = [AllowAny, ]
    elif self.request.method == 'POST':
      self.permission_classes = [IsAuthenticated, ]
    else:
      self.permission_classes = [IsAdminUser, ]
    return super(self.__class__, self).get_permissions()
