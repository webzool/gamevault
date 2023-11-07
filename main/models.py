import os
from django.db import models
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.fields import JSONField
from django.db.models.fields.files import ImageFieldFile
from io import BytesIO
from PIL import Image, ImageOps
from django.utils import timezone
from django.core.files.base import File
# Create your models here.



class Software(models.Model):
    name = models.CharField(max_length=100)
    meta_keywords = models.CharField(max_length=100, blank=True, null=True)
    meta_description = models.TextField()
    content = RichTextUploadingField()
    slug = models.SlugField(max_length=100, unique=True,
                            editable=False, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Software, self).save(*args, **kwargs)

class CompressedImageFieldFile(ImageFieldFile):
    def save(self, name, content, save=True):
        image = Image.open(content)
        image = image.convert('RGB')
        image = ImageOps.exif_transpose(image)
        im_io = BytesIO()
        image.save(im_io, "JPEG", optimize=True, quality=self.field.quality)
        current_datetime = timezone.now()
        filename = os.path.splitext(name)[0]
        filename = f"{filename}{current_datetime}.jpeg"
        image = File(im_io, name=filename)
        super().save(filename, image, save)


class CompressedImageField(models.ImageField):
    attr_class = CompressedImageFieldFile

    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None,
                 quality=50, **kwargs):
        self.quality = quality
        super().__init__(verbose_name, name, width_field, height_field, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.quality:
            kwargs['quality'] = self.quality
        return name, path, args, kwargs



class GamesPage(models.Model):
    meta_keywords = models.CharField(max_length=100, blank=True, null=True)
    meta_description = models.TextField()
    content = RichTextUploadingField()


class ContactPage(models.Model):
    meta_keywords = models.CharField(max_length=100, blank=True, null=True)
    meta_description = models.TextField()
    content = RichTextUploadingField()


class Category(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=150, null=True, blank=True, default=None)
    slug = models.SlugField(null=True, blank=True, default=None, max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

class Tag(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, default=None, max_length=50, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.title)


class Blog(models.Model):
    author = models.ForeignKey("main.Author", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=127)
    slug = models.SlugField('Slug', unique=True, unique_for_date='created_at', null=True, blank=True, max_length=250)
    meta_description = models.TextField(null=True, blank=True)
    meta_keywords = models.CharField(max_length=300, null=True, blank=True)
    meta_title = models.CharField(max_length=100, blank=True, null=True)
    category = models.ManyToManyField(Category,null=True, related_name='category')
    tag =  models.ManyToManyField(Tag)
    image = CompressedImageField(upload_to='blogs/', null=True, blank=True)
    image_alt = models.CharField(max_length=100, blank=True, null=True)
    short_description = models.TextField('Short description', max_length=255, null=True, blank=True)
    content = RichTextUploadingField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField('Is_published', default=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Blog, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = f'{slugify(self.title)}'
        super(Blog, self).save(*args, **kwargs)


class AboutPageContent(models.Model):
    meta_keywords = models.CharField(max_length=127, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    content = RichTextUploadingField()


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class ZohoToken(models.Model):
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f'Token: {self.token} Created At: {self.created_at} Expires At: {self.expires_at}'


class Contact(models.Model):

    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.email)


class AweberLog(models.Model):
    email = models.CharField(max_length=127, blank=True, null=True)
    log = models.TextField(blank=True, null=True)


class AweberCredentials(models.Model):
    client_id = models.CharField(max_length=127, blank=True, null=True)
    client_secret = models.CharField(max_length=127, blank=True, null=True)
    token = JSONField(blank=True, null=True)


class OldBlogSlug(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    old_slug = models.CharField(max_length=125)