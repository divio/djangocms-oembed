# -*- coding: utf-8 -*-
from cms.models import CMSPlugin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
import micawber
from micawber.exceptions import ProviderNotFoundException


providers = micawber.bootstrap_basic()


class OembedVideoPlugin(CMSPlugin):
    oembed_url = models.URLField()
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    autoplay = models.BooleanField(default=False)
    show_related = models.BooleanField(default=False, help_text=_('hiding related videos is not supported by vimeo'))
    loop = models.BooleanField(default=False)


    # this is cached from the request to oembed
    type = models.CharField(max_length=255, blank=True, default='')
    provider = models.CharField(max_length=255, blank=True, default='')
    data = models.TextField(blank=True, default='')
    html = models.TextField(blank=True, default='')

    def clean(self):
        extra = {}
        if self.width:
            extra['maxwidth'] = self.width
        if self.height:
            extra['maxheight'] = self.height
        extra['autoplay'] = self.autoplay
        extra['rel'] = self.show_related
        extra['loop'] = self.loop
        try:
            data = providers.request(self.oembed_url, **extra)
        except ProviderNotFoundException, e:
            raise ValidationError(e.message)
        if not data['type'] == 'video':
            raise ValidationError('This must be an url for a video, not %(type)s.' % {'type': data['type']},)
        self.type = data['type']
        if 'provider' in data:
            self.provider = data['provider']
        self.html = data['html']
        self.data = data


