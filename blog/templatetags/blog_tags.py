from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
register = template.Library()

'''
simple_tag：处理数据并返回一个字符串（string）
inclusion_tag：处理数据并返回一个渲染过的模板（template）
assignment_tag：处理数据并在上下文（context）中设置一个变量(variable)
'''


@register.simple_tag
def total_posts():
    '''
    Django将会使用这个函数名作为标签（tag）名。如果你想使用别的名字来注册这个标签（tag），
    你可以指定装饰器的name属性，比如@register.simple_tag(name='my_tag')
    :return:
    '''
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}



@register.assignment_tag
def get_most_commented_posts(count=5):
    '''
    可以用来解决标签内部无法嵌套的问题
    <h3>Most commented posts</h3>
    {% get_most_commented_posts as most_commented_posts %}
    <ul>
    {% for post in most_commented_posts %}
      <li>
        <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
      </li>
    {% endfor %}
    </ul>
    :param count:
    :return:
    '''
    return Post.published.annotate(
                total_comments=Count('comments')
            ).order_by('-total_comments')[:count]




#  自定义模板过滤器

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))



