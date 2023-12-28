from django.conf import settings
from django.shortcuts import render
import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from .models import MyModel
from .serializers import *
import uuid
from rest_framework import status


#intantiating the s3_client
s3_client = boto3.client('s3',
                        region_name = settings.AWS_S3_REGION_NAME,
                        aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
                    )

bucket_name = settings.AWS_STORAGE_BUCKET_NAME



class CreateMultipartUplaod(APIView):
    def post(self,request):
        try:
            serializer = CreateMultipartUplaodSerializer(data=request.data)
            if serializer.is_valid():

                original_name = serializer.validated_data.get('original_name')
                #todo original_name sligify
                unique_code = str(uuid.uuid1())
                object_path = 'presigned-uploads/' + unique_code + original_name
                create_response = s3_client.create_multipart_upload(
                    Bucket=bucket_name,
                    Key=object_path
                    )
                return Response(create_response,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class GeneratingPresignedUrl(APIView):
    def post(self,request):
        try:

            serializer = GeneratingPresignedUrlSerializer(data=request.data)
            if serializer.is_valid():

                object_path = serializer.validated_data.get('object_path')
                no_of_parts = serializer.validated_data.get('no_of_parts')
                upload_id = serializer.validated_data.get('upload_id')

                signed_urls = []
                for i in range(1, no_of_parts+1):

                    signed_url = s3_client.generate_presigned_url(
                        ClientMethod ='upload_part',
                        Params = {
                            'Bucket': bucket_name,
                            'Key': object_path, 
                            'UploadId': upload_id, 
                            'PartNumber': i
                            }
                        )
                    signed_urls.append(signed_url)
                return Response(signed_urls,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    


class CompleteMultpartUpload(APIView):
    def post(self,request):
        try:
            serializer = CompleteMultpartUploadSerializer(data=request.data)
            if serializer.is_valid():
                
                parts = serializer.validated_data.get('parts')
                upload_id  = serializer.validated_data.get('upload_id')
                object_path = serializer.validated_data.get('object_path')
                
                response = s3_client.complete_multipart_upload(
                    Bucket = bucket_name,
                    Key = object_path,
                    MultipartUpload = {'Parts': parts},
                    UploadId= upload_id
                )
                
                #saving the key in the db
                model_instance = MyModel.objects.create(object_path=object_path)
                model_instance.save()


                return Response({'message':'SUCCESS','response': response},status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#get all for id's
class GetAll(APIView):
    def get(self,request):
        queryset = MyModel.objects.all()
        serializer = MyModelSerializer(queryset,many=True)

        return Response(serializer.data)
    








# class S3DownloadView(APIView):
#     def get(self, request):
        
#         object_key = 'multipart-updated-test/cooking-video-test-1.mp4'
#         # Generate a presigned URL for the object
#         url = s3_client.generate_presigned_url(
#             ClientMethod='get_object',
#             Params={
#                 'Bucket': bucket_name,
#                 'Key': object_key
#             }
#         )

#         # Get the size of the object
#         object_size = int(requests.head(url).headers['Content-Length'])

#         # Set the chunk size to 5MB
#         chunk_size = 5 * 1024 * 1024

#         # Calculate the number of parts required
#         num_parts = object_size // chunk_size + (object_size % chunk_size != 0) #(object_size % chunk_size != 0) True or False os 1 or 0

#         # Create a list to hold the ETag values
#         etags = []
#         file_name = 'downlaod-file.mp4'
#         # Create a multipart download request
#         for i in range(num_parts):
#             start = i * chunk_size
#             end = min(start + chunk_size - 1, object_size - 1)
#             response = requests.get(
#                 url,
#                 headers={'Range': f'bytes={start}-{end}'}
#             )
#             etags.append(response.headers['ETag'])

#             # Write the chunk to the file
#             with open(file_name, 'ab') as f:
#                 f.write(response.content)

#         # Create a complete multipart download request
#         response = s3_client.complete_multipart_download(
#             Bucket=bucket_name,
#             Key=object_key,
#             MultipartUpload={
#                 'Parts': [
#                     {
#                         'ETag': etag,
#                         'PartNumber': i + 1
#                     } for i, etag in enumerate(etags)
#                 ]
#             }
#         )

#         return Response({'message': 'File downloaded successfully!'})



class PresignedDownloadApiview(APIView):
    def get(self,request,id):
        try:

            model_instance = MyModel.objects.get(id=id)
            object_key = model_instance.file_path

            url = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': object_key
                }
            )
            return Response(url,status=status.HTTP_200_OK)
        except MyModel.DoesNotExist:
            return Response({'Not found': 'the requested id does not found in the database'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
