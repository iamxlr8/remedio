from django.http import HttpResponse

def ipfilter(get_response):
    def middleware(request):
        allowed_ips=['127.0.0.1']                    # contains allowed ips
        ip=request.META.get('REMOTE_ADDR')           # retrieval of ip address
        ip1=ip.split('.')
        if ip1[0]=='172':
            allowed_ips.append(ip)                   # add to the list of allowed ips if from IIT BHU
        print(ip)
        if ip not in allowed_ips:
            return HttpResponse('Hold right there Sparky .... You are not from IIT BHU!!')
        response=get_response(request)
        return response
    return middleware
