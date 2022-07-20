from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import get_object_or_404

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_object(self) -> User:
        return get_object_or_404(User, pk=self.kwargs['pk'])

    def list(self, request, *args, **kwargs) -> Response:
        paginated_users = self.paginate_queryset(self.queryset)
        serializer = self.serializer_class(paginated_users, many=True)
        return Response(self.get_paginated_response(serializer.data),HTTP_200_OK)

    def create(self, request, *args, **kwargs) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save_with_password(password=data['password'] if 'password' in data else None)
        return Response(serializer.data, HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, HTTP_200_OK)

    def update(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.update(instance, validated_data=serializer.validated_data)
        return Response(self.serializer_class(updated_instance).data, HTTP_200_OK)

    def destroy(self, request, *args, **kwargs) -> Response:
        self.get_object().delete()
        return Response(HTTP_204_NO_CONTENT)




