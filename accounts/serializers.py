from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")


    def save_with_password(self, **kwargs) -> User:
        """
        In case admin wanted to set password for user despite Password Validation.
        Overrides UserSerializer save method and adds password if it is passed in the request body
        :param kwargs:
        :return: User
        """

        user = super(UserSerializer, self).save()
        if kwargs['password']:
            user.set_password(kwargs['password'])
            user.save()
        return user