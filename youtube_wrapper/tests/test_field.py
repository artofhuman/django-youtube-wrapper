# coding: utf-8
from django.test import TestCase
from django import forms
from django.db import models

from ..fields import YoutubeField


class TestModel(models.Model):
    youtube = YoutubeField()

class TestModelForm(forms.ModelForm):
    class Meta:
        model = TestModel


class FormTest(TestCase):

    def test_validation(self):
        form = TestModelForm(data={'youtube': 'http://youtu.be/jRKrZ6X5WSw'})
        self.assertTrue(form.is_valid())

        invalid = TestModelForm(data={'youtube': 'http://yandex.ru'})
        self.assertFalse(invalid.is_valid())
        self.assertTrue('Invalid youtube url' in str(invalid.errors))

        invalid = TestModelForm(data={'youtube': 'http://youtu.be/'})
        self.assertFalse(invalid.is_valid())
        self.assertTrue('Youtube url has not video param' in str(invalid.errors))


class FieldTest(TestCase):

    def setUp(self):
        self.video_url = 'http://youtu.be/jRKrZ6X5WSw'
        self.field = YoutubeField()

    def test_to_python(self):
        self.res = self.field.to_python(self.video_url)
        self.assertEqual(u'http://youtu.be/jRKrZ6X5WSw', self.res)

    def test_video_id(self):
        self.assertEqual(u'jRKrZ6X5WSw',
                self.field.to_python(self.video_url).video_id)

    def test_embed_url(self):
        expected = u'http://youtube.com/embed/jRKrZ6X5WSw/'
        self.assertEqual(expected,
                self.field.to_python(self.video_url).embed_url)

    def test_images(self):
        default_image_url = 'http://img.youtube.com/vi/jRKrZ6X5WSw/0.jpg'
        thumb_url = 'http://img.youtube.com/vi/jRKrZ6X5WSw/1.jpg'

        self.assertEqual(default_image_url,
                self.field.to_python(self.video_url).default_image_url)

        self.assertEqual(thumb_url,
                self.field.to_python(self.video_url).thumb_url)

