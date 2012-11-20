# -*- coding: utf-8 -*-
from cms.models import CMSPlugin
import pprint
import urllib
import urlparse
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
import micawber
from micawber.exceptions import ProviderNotFoundException, ProviderException
from pyquery import PyQuery

providers = micawber.bootstrap_basic()


class OembedVideoPlugin(CMSPlugin):
    oembed_url = models.URLField(verbose_name=_('url'))
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    autoplay = models.BooleanField(default=False)
    show_related = models.BooleanField(default=False, help_text=_('hiding related videos is not supported by Vimeo (you need vimeo plus)'))
    loop = models.BooleanField(default=False, help_text=_('looping is not supported by YouTube'))

    # cached oembed data
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
        extra['title'] = False  # Vimeo
        extra['byline'] = False  # Vimeo
        extra['portrait'] = False  # Vimeo
        try:
            data = providers.request(self.oembed_url, **extra)
        except ProviderNotFoundException, e:
            raise ValidationError(e.message)
        except ProviderException, e:
            raise ValidationError(e.message)
        if not data['type'] == 'video':
            raise ValidationError('This must be an url for a video. The "%(type)s" type is not supported.' % {'type': data['type']},)
        self.type = data.get('type', '')
        self.provider = data.get('provider_name', '')
        html = data.get('html', '')
        if 'provider_name' in data and self.provider in ['YouTube', 'Vimeo']:
            # dirty special handling of youtube and vimeo.
            # they ignore these parameters over oembed... so we hack them into the iframe url.
            iframe_html = PyQuery(html)
            url = iframe_html.attr('src')
            params = {
                'autoplay': int(self.autoplay),
                'loop': int(self.loop),
                'rel': int(self.show_related),
                'showinfo': 0  # YouTube
            }
            url_parts = list(urlparse.urlparse(url))
            query = dict(urlparse.parse_qsl(url_parts[4]))
            query.update(params)
            url_parts[4] = urllib.urlencode(query)
            new_url = urlparse.urlunparse(url_parts)
            # for some reason this does not work with just an iframe node. And it also urlescapes the src url again
            #iframe_html.attr['src'] = new_url
            #new_html = iframe_html.html(method='html')
            # quick and dirty
            new_html = html.replace(url, new_url)
            html = new_html
        self.html = html
        self.data = data


