from django import template
import re

register = template.Library()

@register.filter
def split(value, arg):
    return value.split(arg)


@register.filter
def trim(value):
    return value.strip() if isinstance(value, str) else value


@register.filter
def youtube_embed(url):
    """
    Convert a standard YouTube URL to an embeddable format.
    """
    match = re.search(r'v=([^&]+)', url)
    if match:
        video_id = match.group(1)
        return f'https://www.youtube.com/embed/{video_id}'
    return url
