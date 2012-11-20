djangocms-oembed
================

A simple oembed plugin.
Currently only video oembeds are implemented. More content types will follow.

Sadly most advanced embedding options (e.g looping) are not supported by most oembed providers.
So there is some special handling for YouTube and Vimeo embeds:

* looping for Vimeo
* no related videos at the end for YouTube