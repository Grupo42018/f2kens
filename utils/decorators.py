from django.http import HttpResponse

def checkGroup(*groups):
    def groupChecker(func):
        def decorator(request, *args, **kwargs):
            userg = request.user.groups.values_list('name', flat=True)
            for group in groups:
                if group in userg:
                    return func(request, *args, **kwargs)
            return HttpResponse("FORBIDDEN",status=403)
        return decorator
    return groupChecker