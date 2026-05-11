from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import WasteReport, Feedback
from .forms import WasteReportForm, FeedbackForm
from accounts.decorators import reporter_required, collector_required, admin_required

CustomUser = get_user_model()

@reporter_required
def reporter_dashboard(request):
    if request.method == 'POST':
        form = WasteReportForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                report = form.save(commit=False)
                report.reporter = request.user
                report.save()
                
                request.user.points += 10
                request.user.save()
                
                messages.success(request, 'Waste report submitted successfully. You earned 10 points!')
                return redirect('reporter_dashboard')
    else:
        form = WasteReportForm()
        
    reports = WasteReport.objects.filter(reporter=request.user).order_by('-created_at')
    return render(request, 'reports/reporter_dashboard.html', {'form': form, 'reports': reports})

@collector_required
def collector_dashboard(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        report = get_object_or_404(WasteReport, id=report_id, status='PENDING')
        form = FeedbackForm(request.POST)
        
        if form.is_valid():
            with transaction.atomic():
                report.status = 'COLLECTED'
                report.collector = request.user
                report.save()
                
                feedback = form.save(commit=False)
                feedback.report = report
                feedback.save()
                
                messages.success(request, 'Waste report marked as collected successfully!')
                return redirect('collector_dashboard')
    else:
        form = FeedbackForm()
        
    pending_reports = WasteReport.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'reports/collector_dashboard.html', {'pending_reports': pending_reports, 'form': form})

@admin_required
def admin_dashboard(request):
    # Handle Collector Approval
    if request.method == 'POST' and 'approve_collector' in request.POST:
        user_id = request.POST.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id, role='COLLECTOR', status='PENDING')
        user.status = 'APPROVED'
        user.save()
        messages.success(request, f'Collector {user.username} approved successfully.')
        return redirect('admin_dashboard')
        
    # Handle Report Verification
    if request.method == 'POST' and 'verify_report' in request.POST:
        report_id = request.POST.get('report_id')
        report = get_object_or_404(WasteReport, id=report_id, status='COLLECTED')
        
        with transaction.atomic():
            report.status = 'VERIFIED'
            report.save()
            
            if report.collector:
                report.collector.points += 20
                report.collector.save()
                messages.success(request, f'Report verified. 20 points awarded to {report.collector.username}.')
            else:
                 messages.warning(request, 'Report verified, but no collector found to award points to.')
                 
        return redirect('admin_dashboard')

    pending_collectors = CustomUser.objects.filter(role='COLLECTOR', status='PENDING')
    collected_reports = WasteReport.objects.filter(status='COLLECTED').order_by('-updated_at')
    
    return render(request, 'reports/admin_dashboard.html', {
        'pending_collectors': pending_collectors,
        'collected_reports': collected_reports
    })

def leaderboard(request):
    top_users = CustomUser.objects.exclude(role='ADMIN').order_by('-points')[:50]
    return render(request, 'reports/leaderboard.html', {'top_users': top_users})
