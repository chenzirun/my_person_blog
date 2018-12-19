
from django.shortcuts import render, HttpResponse
from .models import Contacts
# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def contacts(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact = Contacts(name=name, email=email, subject=subject, message=message)
        contact.save()
        tip = '发送成功！作者会在24小时内回复您！请注意查看您的邮箱！'
        return render(request, 'contacts/index.html', {'tip':tip})
    else:
        render(request, 'blog/contact.html')


