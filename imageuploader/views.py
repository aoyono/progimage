import glob
import mimetypes
import os
import posixpath
import random
import uuid
from pathlib import Path

from PIL import Image
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework import views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response


class FileUploadDownloadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename):
        file_obj = request.data['file']
        uid = uuid.uuid4().hex
        if self._has_format_spec(filename):
            fmt = filename.split(".")[-1]
            uid += '.{}'.format(fmt)
        with open(os.path.join(settings.MEDIA_ROOT, uid), 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        return Response(status=201, data=uid.split(".")[0])

    def get(self, request, uuid, fmt=None):
        path = posixpath.normpath(uuid).lstrip('/')
        fullpath = Path(os.path.join(settings.MEDIA_ROOT, path + (fmt or "")))

        matches = glob.glob1(str(fullpath.parent), "{}*".format(path))
        if not matches:
            raise Http404(
                '"%(image)s" does not exist' % {'image': path})

        if path + (fmt or "") in matches:
            ct = self._get_content_type(fullpath)
            return FileResponse(fullpath.open("rb"), content_type=ct)

        source = random.choice(matches)
        if fmt is not None:
            # transform the image in the desired format
            fullpath = self._convert(source, path + (fmt or ""))
        else:
            # return a random format of the image
            fullpath = fullpath.joinpath(fullpath.parent, source)
        ct = self._get_content_type(fullpath)
        return FileResponse(fullpath.open("rb"), content_type=ct)

    @staticmethod
    def _has_format_spec(filename):
        return len(filename.split(".")) >= 2

    @staticmethod
    def _get_content_type(fullpath):
        content_type, encoding = mimetypes.guess_type(str(fullpath))
        return content_type or 'application/octet-stream'

    @staticmethod
    def _convert(existing, desired):
        src = Path(os.path.join(settings.MEDIA_ROOT, existing))
        dst = Path(os.path.join(settings.MEDIA_ROOT, desired))
        Image.open(str(src)).save(str(dst))
        return dst
