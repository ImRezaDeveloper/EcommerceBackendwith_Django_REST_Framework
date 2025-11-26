from django.db import models
from CommerceCore_project.accounts.models import User

# Create your models here.


class ImageModel(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام عکس')
    image = models.ImageField(upload_to='products')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='تصویر'
        verbose_name_plural = 'تصاویر'


class CategoryModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='دسته بندی')
    slug = models.SlugField(verbose_name='اسلاگ')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='categories', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام محصول')
    description = models.TextField(max_length=300, verbose_name='توضیحات', null=True, blank=True)
    slug = models.SlugField(verbose_name='اسلاگ')
    price = models.FloatField(verbose_name='قیمت', null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name='تعداد', default=2, null=True, blank=True)
    discount_percent = models.PositiveIntegerField(default=30, verbose_name='کد تخفیف', null=True, blank=True)
    images = models.ManyToManyField(ImageModel, related_name='products', verbose_name='عکس ها', null=True, blank=True)
    categories = models.ManyToManyField(CategoryModel, related_name='products', verbose_name='دسته بندی ها', null=True, blank=True)
    user = models.ForeignKey(User, related_name='products', verbose_name='کاربر', on_delete=models.CASCADE,null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name='فعال؟')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='محصول'
        verbose_name_plural = 'محصولات'