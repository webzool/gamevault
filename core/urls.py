from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import Sitemap
from main.sitemaps import SoftwareSitemap, StaticSitemap, BlogSitemap
from django.views.generic import TemplateView

sitemaps = {
    'software': SoftwareSitemap,
    'static': StaticSitemap,
    'blog': BlogSitemap
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('',include('main.urls', namespace='core')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'gamevaultcasino Casino Admin'
admin.site.site_title = 'gamevaultcasino Casino  Administration'
admin.site.index_title = 'gamevaultcasino Casino  Administration'