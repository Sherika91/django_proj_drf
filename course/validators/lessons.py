import re

from rest_framework.serializers import ValidationError


class OnlyYouTubeUrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        description = dict(value).get(self.field)

        links_patter = r'(https?://[^\s]+)'
        youtube_pattern = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'

        links = re.findall(links_patter, description)
        for link in links:
            if not bool(re.match(youtube_pattern, link)):
                raise ValidationError('Only YouTube links are allowed, your link: {}'.format(value['video']))
