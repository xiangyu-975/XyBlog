import markdown
from django.urls import reverse
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils.html import strip_tags


class Category(models.Model):
    '''
    django要求模型必须继承models.Model
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    当然 django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
    django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types
    '''
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    '''
    标签Tag也比较简单 和category一样
    再次强调一定要继承models.Model
    '''
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    '''
    文章数据库稍微复杂，需要更多字段
    '''
    # 文章标题
    title = models.CharField('标题', max_length=70)
    # 正文使用了Textfield
    # 存储比较短的字符串可以使用CharField，但是对于文章的正文来说会是一大段文字，因此使用TextField来存储大段文字
    body = models.TextField('正文')

    # 这两个列分别代表文章创建时间和最后一次修改时间，使用DateTimeField字段
    create_time = models.DateTimeField('创建时间', default=timezone.now())
    modified_time = models.DateTimeField('修改时间')

    # 文章摘要 可以没有文章摘要，但默认情况瞎，CharField要求我们必须存入数据，否则就会报错
    # 指定CharField的blank=True 参数值后就可以允许空值了
    excerpt = models.CharField('摘要', max_length=200, blank=True)

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        # 首先实例化一个Markdown类，用于渲染body文本
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 先将Markdown文本渲染成HTML文本
        # strip_tags 去掉HTML 文本的全部HTML标签
        # 从文本摘取前54个字符赋给excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一
    # 对多的关联关系。且自 django 2.0 以后，ForeignKey 必须传入一个 on_delete 参数用来指定当关联的
    # 数据被删除时，被关联的数据的行为，我们这里假定当某个分类被删除时，该分类下全部文章也同时被删除，因此
    # 使用 models.CASCADE 参数，意为级联删除。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用
    # ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/2.2/topics/db/models/#relationships

    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    # 文章作者 这里User是从django.contrib.auth.models导入的
    # django.contrib.auth 是django内置的应用，专门用于处理用户网站的注册，登录等流程，User是django为我们已经写好的用户模型
    # 这里我们通过ForeignKey 把文章和User 关联了起来
    # 因为我们规定一篇文章只能有一个作者，而一个作者可以有多篇文章，因此这是一对多的关系，和category类似
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_time', 'title']

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
