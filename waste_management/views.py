from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.role == 'REPORTER':
        return redirect('reporter_dashboard')
    elif request.user.role == 'COLLECTOR':
        if request.user.status == 'PENDING':
            return render(request, 'pending_approval.html')
        return redirect('collector_dashboard')
    elif request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    
    return redirect('home')
