from verify.models import CheckOut


def check_count(requqest):
    check_count = CheckOut.objects.all().filter(status=False).count()
    return {'check_count': check_count}
