from django.conf import settings
from rest_framework import serializers
from django.db.models import Avg
from .models import Course, Teacher, Review
from accounts.serializers import UserSerializer
from mysite.paginator import MyCustomPaginator
from django.db.models.query import QuerySet

class CourseSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField(read_only=True)
    review_point_average = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'created',
            'updated',
            'title',
            'description',
            'teacher',
            'price',
            'published_at',
            'review_count',
            'review_point_average'
        ]

    @staticmethod
    def reviews(obj) -> QuerySet:
        return Review.objects.filter(course=obj)

    def get_review_count(self, obj) -> int:
        review_count = self.reviews(obj).count()
        return review_count

    def get_review_point_average(self,obj):
        reviews = self.reviews(obj)
        avg = reviews.aggregate(avg=Avg('score'))['avg']
        return round(avg,2) if avg else "Not Scored"

    def validate(self, attrs) -> dict:
        if attrs.get('price') < 10000:
            raise serializers.ValidationError({'Price': 'Course price lower than 10,000 toman is not permitted.'})
        return attrs


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    courses = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Teacher
        fields = "__all__"


    def get_courses(self,obj) -> dict:
        queryset = obj.course_set.all()
        request = self.context.get('request')
        serializer = CourseSerializer(queryset, many=True)
        paginator = MyCustomPaginator()
        paginated_data = paginator.paginate_queryset(queryset=serializer.data, request=request)
        result = paginator.get_paginated_response(paginated_data)
        return result


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    course = CourseSerializer()

    class Meta:
        model = Review
        fields = "__all__"
