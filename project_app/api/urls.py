from django.urls import path
from . import views

urlpatterns = [
  path('projects/', views.Projects.as_view(), name='projects'),
  path('new-project/', views.ProjectNew.as_view(), name='new-project'),
  path('project-delete/<int:id>/', views.DeleteProjct.as_view(), name='delete-project'),
  path('detail/<int:id>', views.DetailProject.as_view(), name='project-detail'),
  path('<int:id>/export-pdf/', views.export_project_pdf.as_view(), name='export_project_pdf'),
  path('summarize-text/', views.SummarizeText.as_view(), name='summarize_text'),
  path('share/', views.ShareProject.as_view(), name='share-project')
]
