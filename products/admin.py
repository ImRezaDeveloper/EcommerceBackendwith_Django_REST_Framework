from django.contrib import admin
from .models import CategoryModel, ProductModel, ImageModel, CommentProduct, WishListProduct
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(CategoryModel)
admin.site.register(ProductModel, ProductAdmin)
admin.site.register(ImageModel)
admin.site.register(CommentProduct)
admin.site.register(WishListProduct)