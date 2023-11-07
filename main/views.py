import requests
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView
from django.conf import settings
import os
from .models import AboutPageContent, Blog, Category, Contact, ContactPage, GamesPage, Software, OldBlogSlug, Tag
from main.serializers import AweberCredentialsSerializer
from django.shortcuts import render
from .zoho_client import ZohoClient
from django.shortcuts import render, get_object_or_404
from main.aweber.utils import add_subscriber
import logging
import requests
from rest_framework.response import Response
from .models import AweberCredentials
from rest_framework import status
from rest_framework.decorators import api_view


# Create your views here.


def base(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        myobj = {'secret': settings.RECAPTCHA_SECRET_KEY,
                 'response': recaptcha_response}
        x = requests.post(url, data=myobj)
        name = request.POST.get('name').split()
        first_name = name[0]
        try:
            last_name = name[1]
        except:
            last_name = "."
        message = request.POST.get('message')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        name = request.POST.get('name').split()
        full_name = first_name + " " + last_name
        Contact.objects.create(
            full_name=full_name, email=email, phone=phone, subject=subject, message=message)
        
        if x.json()['success']:
            data = [{
                'Title': subject,
                'Lead_Source': "gamevault-casino.com",
                'Mobile': phone,
                'First_Name': first_name,
                'Last_Name': last_name,
                'Email': email,
                'Description': message
            }]
            zoho_client = ZohoClient()
            zoho_client.crmAddNew("Leads", data)
            try:
                add_subscriber(email=email, phone=phone, full_name=full_name, tags=subject)
            except:
                logging.error("Failed to add subscriber to aweber")
            return redirect('main:thank_you')
        return render(request, 'base.html')
    return render(request, 'base.html')


def home(request):
    if request.method == 'POST':
        print('Home request')
        recaptcha_response = request.POST.get('g-recaptcha-response')
        print(recaptcha_response, 'recaptcha_response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        myobj = {'secret': '6LcxWx8iAAAAAE5l2NPP4MJLTmINRL4uzcjkvDsU',
                 'response': recaptcha_response}
        x = requests.post(url, data=myobj)
        name = request.POST.get('name').split()
        first_name = name[0]
        try:
            last_name = name[1]
        except:
            last_name = "."
        message = request.POST.get('message')
        email = request.POST.get('email')
        phone = f"1{request.POST.get('phone')}"
        subject = request.POST.get('subject')
        name = request.POST.get('name').split()
        full_name = first_name + " " + last_name

        Contact.objects.create(
            full_name=full_name, email=email, phone=phone, subject=subject, message=message)
        print(x.json())
        if x.json()['success']:
            data = [{
                'Title': subject,
                'Lead_Source': "gamevault-casino.com",
                'Mobile': phone,
                'First_Name': first_name,
                'Last_Name': last_name,
                'Email': email,
                'Description': message
            }]
            zoho_client = ZohoClient()
            zoho_client.crmAddNew("Leads", data)
            try:
                add_subscriber(email=email, phone=phone, full_name=full_name, tags=subject)
            except:
                logging.error("Failed to add subscriber")
            return redirect('main:thank_you')
        return render(request, 'home.html')
    return render(request, 'home.html')


def thank_you(request):
    return render(request, 'thank-you.html')




class BlogPageContentView(ListView):
    template_name = 'blog.html'
    context_object_name = 'blogs'
    paginate_by = 10
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_blogs'] = Blog.objects.filter(is_published=True)[:3]
        search = self.request.GET.get('search')
        # queryset = Blog.objects.filter(is_published=True)
        if search:
            queryset = Blog.objects.filter(
                is_published=True, title__icontains=search)
            context['blogs'] = queryset
        return context


class BlogCategoryListView(ListView):
    template_name = 'blog-category.html'
    context_object_name = 'blogs'
    paginate_by = 10
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_blogs'] = Blog.objects.filter(is_published=True)[:3]
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        # queryset = Blog.objects.filter(is_published=True, category=category)
        search = self.request.GET.get('search')
        if search:
            queryset = Blog.objects.filter(
                is_published=True, title__icontains=search)
            context['blogs'] = queryset
        return context


class BlogTagListView(ListView):
    template_name = 'blog-tag.html'
    context_object_name = 'blogs'
    paginate_by = 10
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()[:10]
        context['recent_blogs'] = Blog.objects.filter(is_published=True)[:3]
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        queryset = Blog.objects.filter(is_published=True, tag=tag)
        context['blogs'] = queryset
        return context


def blog_detail(request, slug):
    context = {}
    queryset = Blog.objects.filter(is_published=True, slug=slug).last()
    if not queryset:
        blog = OldBlogSlug.objects.filter(old_slug=slug).last()
        queryset = Blog.objects.filter(is_published=True, id=blog.id).last()
    context['blog'] = queryset
    context['related_blogs'] = Blog.objects.filter(
        is_published=True, category__in=queryset.category.all()).exclude(id=queryset.id)
    context['recent_blogs'] = Blog.objects.filter(is_published=True)[:3]
    context['tags'] = Tag.objects.all()
    return render(request, "blog-detail.html", context)


class AboutPageContentView(TemplateView):
    template_name = 'about-us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["about_content"] = AboutPageContent.objects.last()
        return context


class GamePageContentView(TemplateView):
    template_name = 'games-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["game_content"] = GamesPage.objects.last()
        return context


class ContactPageContentView(TemplateView):
    template_name = 'contact-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_content"] = ContactPage.objects.last()
        return context


class SoftwareDetailsView(DetailView):
    template_name = 'software-details.html'
    model = Software
    context_object_name = 'software'


class BannerPage(TemplateView):
    template_name = 'banner.html'


class TermsPageContentView(TemplateView):
    template_name = 'terms.html'


class PrivacyPageContentView(TemplateView):
    template_name = 'privacy.html'


class ThankYou(TemplateView):
    template_name = 'thank-you.html'


class Faq(TemplateView):
    template_name = 'faq.html'

class DownloadApp(TemplateView):
    template_name = 'download-app.html'
class NotFound(TemplateView):
    template_name = 'not-found.html'

@api_view(['GET'])
def get_aweber_credentials(request):
    data = request.data
    if data.get('api_key') == os.getenv('AWEBER_API_KEY'):
        obj = AweberCredentials.objects.last()
        serializer = AweberCredentialsSerializer(obj)
        credentials = serializer.data
        AweberCredentials.objects.create(
        client_id=credentials['client_id'],
        client_secret=credentials['client_secret'],
        token=credentials['token']
        )
        AweberCredentials.objects.first().delete()
        return Response(serializer.data)
    return Response({'detail': 'Access is required for this endpoint'}, status=status.HTTP_400_BAD_REQUEST)
