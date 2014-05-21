from assign.models import Assign

__author__ = 'soroosh'


def notification(request):
    assigns = Assign.objects.filter(target__id=request.user.id)
    return {'notifications': assigns}
