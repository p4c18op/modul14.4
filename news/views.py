from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import New, News, Subscription
from .forms import NewForm
from .filters import NewFilter
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.db.models import Exists, OuterRef
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.translation import gettext as _


@cache_page(60 * 15) # в аргументы к декоратору передаём количество секунд, которые хотим, чтобы страница держалась в кэше. Внимание! Пока страница находится в кэше, изменения, происходящие на ней, учитываться не будут!
def my_view(request):
    ...


class NewsList(ListView):
    model = New
    ordering = 'name'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
class NewDetail(DetailView):
    model = New
    template_name = 'new.html'
    context_object_name = 'new'


class NewCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_new',)
    form_class = NewForm
    model = New
    template_name = 'new_edit.html'


class NewUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_new',)
    form_class = NewForm
    model = New
    template_name = 'new_edit.html'


class NewDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_new',)
    model = New
    template_name = 'new_delete.html'
    success_url = reverse_lazy('new_list')

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        news_id = request.POST.get('news_id')
        news = News.objects.get(id=news_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, news=news)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                news=news,
            ).delete()

    news_with_subscriptions = News.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                news=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'news': news_with_subscriptions},
    )


class NewDetailView(DetailView):
    template_name = 'news/new_detail.html'
    queryset = New.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'new-{self.kwargs["pk"]}', None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'new-{self.kwargs["pk"]}', obj)
            return obj

class MobileOrFullMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.mobile:
            prefix = "mobile/"
        else:
            prefix = "full/"
        response.template_name = prefix + response.template_name
        return response

class Index(View):
    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)


