from rest_framework import serializers
from .models import RatingOptions, Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    synopsis = serializers.CharField(required=False)
    rating = serializers.ChoiceField(choices=RatingOptions.choices, required=False)
    duration = serializers.CharField(max_length=10, required=False)
    added_by = serializers.CharField(source="user.email", read_only=True)

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
