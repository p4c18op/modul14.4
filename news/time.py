from django.utils import timezone
import pytz


def timezone_context_processor(request):
    context = {
        'current_time': timezone.localtime(timezone.now()),
        'timezones': pytz.common_timezones,
    }
    return context