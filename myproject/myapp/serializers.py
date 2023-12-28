from rest_framework import serializers

from .models import MyModel



class CreateMultipartUplaodSerializer(serializers.Serializer):
    original_name = serializers.CharField(max_length=255)
    content_type = serializers.CharField(max_length=255)

    def validate_content_type(self,content_type):
        allowed_formats = ['image/jpeg', 'video/mp4','application/pdf', 'application/docx', 'application/txt']
        if content_type not in allowed_formats:
            raise serializers.ValidationError(f'content type should in {allowed_formats} only')


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