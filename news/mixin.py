import pytz
from django.shortcuts import redirect
from django.utils import timezone


class TimeZoneMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request, pk=None):
        try:
            tz = request.POST['timezone']
            request.session['django_timezone'] = request.POST['timezone']
        except KeyError:
            pass
        return redirect(self.request.path)