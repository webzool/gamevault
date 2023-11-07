from django.urls import path
from main.views import (AboutPageContentView, Faq, BlogPageContentView, BlogCategoryListView,
                        BlogTagListView,
                        PrivacyPageContentView, GamePageContentView, ContactPageContentView, SoftwareDetailsView,
                        ThankYou,DownloadApp ,NotFound,TermsPageContentView, base, home, thank_you, get_aweber_credentials,blog_detail)

app_name = 'main'

urlpatterns = [
    path('terms-and-conditions/', TermsPageContentView.as_view(),
         name='terms-and-conditions'),
    path('privacy-policy/', PrivacyPageContentView.as_view(), name='privacy-policy'),
    path('about/', AboutPageContentView.as_view(), name='about'),
    path('games/', GamePageContentView.as_view(), name='games'),
    path('faq/', Faq.as_view(), name='faq'),
    path('contact/', ContactPageContentView.as_view(), name='contact'),
    path('thank-you', thank_you, name='thank_you'),
    path('', home, name='home'),
    path('', base, name='base'),
    path('software/<slug:slug>/',
         SoftwareDetailsView.as_view(), name='software-detail'),
     path('download-app/', DownloadApp.as_view(), name='download-app'),
    path('not-found/', NotFound.as_view(), name='not-found'),
    path('thank-you/', ThankYou.as_view(), name='thank-you'),
    path('blog/', BlogPageContentView.as_view(), name="blogs"),
    path('blog-categories/<slug:slug>/', BlogCategoryListView.as_view(), name='blog-category-list'),
    path('blog-tags/<slug:slug>', BlogTagListView.as_view(), name='blog-tag-list'),
    path('blog/<slug:slug>/', blog_detail, name="blog-detail"),
    path('get-aweber-credentials/', get_aweber_credentials,)

]