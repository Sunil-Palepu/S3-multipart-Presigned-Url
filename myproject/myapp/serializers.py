from rest_framework import serializers

from .models import MyModel



class CreateMultipartUplaodUploadSerializer(serializers.Serializer):
    original_name = serializers.CharField(max_length=255)
    content_type = serializers.CharField(max_length=255)

    def validate_content_type(self,content_type):
        allowed_formats = ['image/jpeg', 'video/mp4']
        if content_type not in allowed_formats:
            raise serializers.ValidationError('content type should be image/jpeg or video/mp4')


class GeneratingPresignedUrlSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=255)
    no_of_parts = serializers.IntegerField()
    upload_id = serializers.CharField(max_length=255)



class CompleteMultpartUploadSerializer(serializers.Serializer):
    parts = serializers.ListField()
    upload_id = serializers.CharField(max_length=255)
    key = serializers.CharField(max_length=255)
     


class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'