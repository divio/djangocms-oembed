# -*- coding: utf-8 -*-
from micawber import ProviderRegistry, Provider, bootstrap_basic


def bootstrap(cache=None):
    # micawbers own bootstrap basic plus some more
    pr = bootstrap_basic(cache=cache)
    # add https support for vimeo and youtube
    pr.register('https://vimeo.com/\S*', Provider('https://vimeo.com/api/oembed.json'))
    pr.unregister('https?://(\S*.)?youtu(\.be/|be\.com/watch)\S+')
    pr.register('https?://(\S*.)?youtu(\.be/|be\.com/watch)\S+', Provider('https://www.youtube.com/oembed?scheme=https'))
    return pr

