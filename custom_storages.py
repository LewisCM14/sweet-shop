"""
This module is for AWS and Django settings using Boto

when the project is deployed to Heroku.
Heroku will run python3 manage.py collectstatic during the build process.
Which will search through all apps and project folders
looking for static files. It will use the s3 custom domain in settings.py.
In conjunction with the custom storage classes,
that tell it the location at that URL, where to store static files.

In effect when the USE_AWS setting is true.
Whenever collectstatic is run.
Static files will be collected into a static folder in the S3 bucket.

"""

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    custom class called static storage.
    inherits from django storages. Giving it all its functionality.
    tells django we want to store static files
    in a location from the settings.
    """
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """
    custom class called media storage.
    inherits from django storages. Giving it all its functionality.
    tells django we want to store media files
    in a location from the settings.
    """
    location = settings.MEDIAFILES_LOCATION
