from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ConsultationCase, CaseComment
from .forms import ConsultationCaseForm, CaseCommentForm

@login_required
def case_list(request):
    # Show different views based on user type
    user = request.user
    
    if user.profile.user_type == 'consultant':
        cases = user.assigned_cases.all().order_by('-created_at')
    else:
        cases = user.consultation_cases.all().order_by('-created_at')
    
    context = {
        'cases': cases,
    }
    return render(request, 'consultants/cases.html', context)

@login_required
def case_detail(request, pk):
    case = get_object_or_404(ConsultationCase, pk=pk)
    
    # Security check: only consultants assigned to the case or the case creator can view it
    if request.user != case.client and request.user != case.consultant:
        messages.error(request, "You don't have permission to view this case.")
        return redirect('case_list')
    
    if request.method == 'POST':
        comment_form = CaseCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.case = case
            comment.user = request.user
            comment.save()
            return redirect('case_detail', pk=case.pk)
    else:
        comment_form = CaseCommentForm()
    
    comments = case.comments.all().order_by('created_at')
    
    context = {
        'case': case,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'consultants/case_detail.html', context)

@login_required
def create_case(request):
    if request.method == 'POST':
        form = ConsultationCaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.client = request.user
            case.save()
            messages.success(request, 'Your consultation case has been created successfully!')
            return redirect('case_detail', pk=case.pk)
    else:
        form = ConsultationCaseForm()
    
    return render(request, 'consultants/create_case.html', {'form': form})
# Create your views here.
