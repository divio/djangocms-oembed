# -*- coding: utf-8 -*-
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from .models import OembedVideoPlugin
from django.utils.translation import ugettext_lazy as _


class CMSOembedVideoPlugin(CMSPluginBase):
    name = _('Video (embedded)')
    model = OembedVideoPlugin
    render_template = 'djangocms_oembed/plugins/video.html'
    admin_preview = False
    text_enabled = True
    fieldsets = (
        (None, {'fields': ('oembed_url', ('width', 'height',), 'autoplay', 'show_related',)}),
        ('advanced', {'fields': ('type', 'html', 'data')}),
    )
    readonly_fields = ('type', 'html', 'data',)

plugin_pool.register_plugin(CMSOembedVideoPlugin)
