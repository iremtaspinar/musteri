from .models import ActivityLog
class ActivityLogMiddleware:
    def __init__(self,get_response): self.get_response=get_response
    def __call__(self,request):
        response=self.get_response(request)
        try:
            if request.user.is_authenticated and request.method in ['POST','PUT','PATCH','DELETE']:
                ActivityLog.objects.create(user=request.user,path=request.path[:500],method=request.method,description='Kullanıcı veri değişikliği yaptı.',ip_address=self.get_client_ip(request))
        except Exception: pass
        return response
    def get_client_ip(self,request):
        x=request.META.get('HTTP_X_FORWARDED_FOR')
        return x.split(',')[0] if x else request.META.get('REMOTE_ADDR')
