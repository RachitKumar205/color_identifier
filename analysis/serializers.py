from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

class ColorResultSerializer(serializers.Serializer):
    URO = serializers.ListField(child=serializers.IntegerField(), min_length=3, max_length=3)
    BIL = serializers.ListField(child=serializers.IntegerField(), min_length=3, max_length=3)
    KET = serializers.ListField(child=serializers.IntegerField(), min_length=3, max_length=3)
    BLD = serializers.ListField(child=serializers.IntegerField(), min_length=3, max_length=3)
    PRO = serializers.ListField(child=serializers.IntegerField(), min_length=3, max_length=3)
    NIT = serializers.ListField(child=serializers.IntegerField(), min_length=3, max_length=3)
    LEU = serializers.ListField(child=serializers.IntegerField(), min_length=3, max_length=3)
    GLU = serializers.ListField(child=serializers.IntegerField(), min_length=3, max_length=3)
    SG = serializers.ListField(child=serializers.IntegerField(), min_length=3, max_length=3)
    PH = serializers.ListField(child=serializers.IntegerField(), min_length=3, max_length=3)