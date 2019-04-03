import uuid

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APISimpleTestCase


class ImageUploaderTests(APISimpleTestCase):

    def test_image_upload(self):
        image = SimpleUploadedFile("image.jpg", b"image content",
                                   content_type="image/jpeg")
        response = self.client.post("/image.jpg", data=image)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(uuid.UUID(response.body.decode("utf-8")))

    def test_image_download(self):
        pass

