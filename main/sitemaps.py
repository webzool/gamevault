from django.contrib.sitemaps import Sitemap
from main.models import Software, Blog


class Site:
    domain = 'gamevault-casino.com'
    name = 'gamevault-casino.com'

    def __str__(self):
        return self.domain


class SoftwareSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def get_urls(self, site=None, protocol=None, **kwargs):
        return super().get_urls(site=Site(), protocol='https', **kwargs)

    def items(self):
        return Software.objects.all()


    def location(self, obj):
        return f'/software/{obj.slug}/' 


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def get_urls(self, site=None, protocol=None, **kwargs):
        return super().get_urls(site=Site(), protocol='https', **kwargs)

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return f'/blog/{obj.slug}/'


class StaticSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.8
    protocol = 'https'

    def get_urls(self, site=None, protocol=None, **kwargs):
        return super().get_urls(site=Site(), protocol='https', **kwargs)

    def items(self):
        return ['/',
                # '/blog',
                '/about/',
                '/contact/',
                '/games/',
                '/privacy-policy/',
                '/terms-and-conditions/',
                '/faq/',
                '/blog/',
                '/privacy-policy/',
                '/download-app/',
                ]

    def location(self, obj):
        return obj