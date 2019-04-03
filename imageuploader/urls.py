# -*- coding: utf-8 -*-
from django.urls import path, re_path

from imageuploader.views import FileUploadDownloadView

urlpatterns = [
    path('<str:filename>', FileUploadDownloadView.as_view()),
    re_path(r'(?P<uuid>\w+)(?P<fmt>.\w{3})?/$', FileUploadDownloadView.as_view()),
]
