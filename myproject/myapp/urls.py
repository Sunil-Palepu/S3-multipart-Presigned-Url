from django.contrib import admin
from django.urls import path,include
from .views import *




urlpatterns = [
    
    path('createmultipartuplaod/',CreateMultipartUplaod.as_view()),
    path('generatepresignedurl/',GeneratingPresignedUrl.as_view()),
    path('completemuiltipartupload/',CompleteMultpartUpload.as_view()),
    # path('presignedurltodownload/',S3DownloadView.as_view()),
    path('getall/', GetAll.as_view()),
    path('presigneddownloadapiview/<int:id>', PresignedDownloadApiview.as_view()),
]
