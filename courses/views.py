from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.mixins import ListModelMixin
from .permissions import IsOwnerOrAdmin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_201_CREATED
from .serializers import CourseSerializer, TeacherSerializer, ReviewSerializer
from .models import Course, Teacher, Review
from rest_framework.decorators import action


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related('teacher','teacher__user')
    serializer_class = CourseSerializer

    def get_object(self) -> Course:
        return get_object_or_404(Course, pk=self.kwargs['pk'])

    def get_permissions(self) -> list:
        """
        Returns a list of Permissions based on the action
        :return:
        """
        permission_classes = [AllowAny] if self.action in ['list', 'retrieve'] else [IsAdminUser] if self.action in ['create', 'destroy'] else [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, HTTP_200_OK)

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, HTTP_200_OK)

    def update(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        self.check_object_permissions(request=self.request, obj=instance)
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.update(instance, validated_data=serializer.validated_data)
        return Response(self.serializer_class(updated_instance).data, HTTP_200_OK)

    def destroy(self, request, *args, **kwargs) -> Response:
        self.get_object().delete()
        return Response(HTTP_204_NO_CONTENT)


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_object(self) -> Teacher:
        return get_object_or_404(Teacher, pk=self.kwargs['pk'])

    @action(detail=True, name='Get Teacher Courses', permission_classes=[AllowAny])
    def courses(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_object(), context={'request': request})
        return Response(serializer.data, HTTP_200_OK)


class ReviewViewSet(GenericViewSet,
                    ListModelMixin):
    queryset = Review.objects.select_related('course','user')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs) -> Response:
        reviews = self.queryset.filter(user=request.user)
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data, HTTP_200_OK)



