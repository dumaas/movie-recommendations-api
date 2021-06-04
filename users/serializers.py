from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
  url = serializers.HyperlinkedIdentityField(
      view_name='users-detail',
  )

  class Meta:
    model = CustomUser
    fields = (
        'url',
        'id',
        'email',
        'first_name',
        'ratings')


class CustomUserRegistrationSerializer(RegisterSerializer):
  first_name = serializers.CharField(required=False)
  last_name = serializers.CharField(required=False)

  def custom_signup(self, request, user):
    user.first_name = self.validated_data.get('first_name', '')
    user.last_name = self.validated_data.get('last_name', '')
    user.save(update_fields=['first_name', 'last_name'])
    return user
