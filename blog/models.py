from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager


# 自定义模型管理器
class PublishedManager(models.Manager):
    '''
    >>> from blog.models import Post
    >>> Post.published.all()
    >>> <QuerySet []>
    '''
    def get_queryset(self):
        return super().get_queryset().filter(status='published')



class Post(models.Model):

    objects = models.Manager()  # 显式声明
    published = PublishedManager()

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250, verbose_name="标题")

    # 不能理解为标签
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        ordering = ('-publish',)
        verbose_name_plural = "博客"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        '''
        我们通过使用strftime()方法来保证个位数的月份和日期需要带上0来构建URL（译者注：也就是01,02,03）
        我们将会在我们的模板（templates）中使用get_absolute_url()方法
        :return:
        '''
        return reverse('blog:post_detail',
                       args=[self.publish.year, self.publish.strftime('%m'), self.publish.strftime('%d'), self.slug])

    # 引入标签管理器
    tags = TaggableManager()

class Comment(models.Model):
    '''
    related_name属性允许我们给这个属性命名，这样我们就可以利用这个关系从相关联的对象反向定位到这个对象。定义好这个之后，
    我们通过使用 comment.post就可以从一条评论来取到对应的帖子，以及通过使用post.comments.all()来取回一个帖子所有的评论。
    如果你没有定义related_name属性，Django会使用这个模型（model）的名称加上_set（在这里是：comment_set）
    我们用一个active布尔字段用来手动禁用那些不合适的评论。默认情况下，我们根据created字段，对评论按时间顺序进行排序。

    '''
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = "评论"

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
