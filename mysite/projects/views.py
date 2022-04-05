from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from projects.models import Project

def project_index(request):
    projects = Project.objects.all()
    context={
        'projects':projects
    }
    
    response = render(request,'projects/index.html',context)
    return response

# def project_detail(request,pk):
#     project = get_object_or_404(Project, pk=pk)
#     context = {
#         'project':project
#     }
#     return render(request,'projects/detail.html',context)

class ProjectDetail(DetailView):
    model = Project
    template_name = 'projects/projects_detail.html'   