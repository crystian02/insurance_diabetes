from django.shortcuts import render

def dashboard(request):
    tab = request.GET.get('tab', 'insurance')
    return render(request, 'ml/dashboard.html', {'tab': tab})