from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

from blog.models import Post

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_post.html')
def show_latest_post(count=5):
    latest_post = Post.published.order_by('-publish')[:count]
    return {'latest_post': latest_post}

@register.assignment_tag
def get_most_commented_post(count=5):
    return Post.published.annotate(total_comments=Count('comments'))\
                         .order_by('-total_comments')[:count]

@register.filter
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
