from rest_framework.serializers import ModelSerializer, Serializer
from quiz.models import Quiz, Question, Answer, Science



class ScienceSerializer(ModelSerializer):
    class Meta:
        model = Science
        fields = ['id', 'name']