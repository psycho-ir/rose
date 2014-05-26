from assign.models import Assign

__author__ = 'soroosh'


def notification(request):
    count = Assign.objects.filter(target__id=request.user.id, status='pending').count()
    return {'notifications_count': count}
