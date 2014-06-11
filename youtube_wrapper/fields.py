# coding: utf-8
import re

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _


def validate_youtube_url(value):
    """
    http://stackoverflow.com/questions/2964678/jquery-youtube-url-validation-with-regex
    """
    pattern = r'^http:\/\/(?:www\.)?youtube.com\/watch\?(?=.*v=\w+)(?:\S+)?$'

    if value[:16] == 'http://youtu.be/':
        if re.match(r'\w+', value[16:]) is None:
            raise forms.ValidationError(_('Youtube url has not video param'))
    elif re.match(pattern, value) is None:
        raise forms.ValidationError(_('Invalid youtube url'))


class YoutubeUrl(object):

    def __init__(self, url):
        self.origin_url = url
        self.parsed_url = urlparse.urlparse(url)

    @property
    def video_id(self):
        if self.is_share_url():
            return self.parsed_url.path.replace('/', '')

    @property
    def embed_url(self):
        return 'http://youtube.com/embed/%s/' % self.video_id

    @property
    def thumb_url(self):
        return "http://img.youtube.com/vi/%s/1.jpg" % self.video_id

    @property
    def default_image_url(self):
        return "http://img.youtube.com/vi/%s/0.jpg" % self.video_id

    def is_share_url(self):
        """
        Returns True if youtube url coped from share
        and looks like this 'http://youtube.com/embed/jRKrZ6X5WSw/'
        """
        return bool(self.parsed_url.netloc == 'youtu.be')


class YoutubeField(models.URLField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(YoutubeField, self).__init__(*args, **kwargs)
        self.validators.append(validate_youtube_url)

    def to_python(self, value):
        url = super(YoutubeField, self).to_python(value)
        return YoutubeUrl(url)

    def get_prep_value(self, value):
        return str(value)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([],  ["^youtube_wrapper\.fields\.YoutubeField"])
except ImportError:
    pass
