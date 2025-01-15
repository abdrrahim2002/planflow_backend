from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProjectSerializers
from .permissions import AuthUserPermission
from .. import models
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests
from django.core.mail import EmailMessage

import os
import logging
logging.basicConfig(level=logging.DEBUG)

#list of Projects
class Projects(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes = [TokenAuthentication]
  
  def get(self, request):
    projects = models.Project.objects.all()
    serializer = ProjectSerializers(projects.filter(user=request.user), many=True)
    return Response(serializer.data)


#add new project
class ProjectNew(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [MultiPartParser, FormParser]
  authentication_classes = [TokenAuthentication]
  
  def post(self, request, format=None):
    
    data = request.data.copy()
    serializer = ProjectSerializers(data = data)
    
    print(request.data)
    
    if serializer.is_valid():
      serializer.save(user=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    else :
      content = {'error':'could not save it'}
      return Response (content, status=status.HTTP_400_BAD_REQUEST)    


#delete project
class DeleteProjct(APIView):
  permission_classes = [IsAuthenticated, AuthUserPermission]
  authentication_classes = [TokenAuthentication]
  
  def delete(self, request, id):
    try:
      project = models.Project.objects.get(id=id)
      
      #delete the image for the upload folder
      project.deleteImage1()
      project.deleteImage2()
      
      #delete the rest of data
      project.delete()
      
      context = {'message': 'delete successfully'}
      return Response (context, status=status.HTTP_204_NO_CONTENT)
    
    except models.Project.DoesNotExist:
      context = {'error': 'could not delete'}
      return Response (context, status=status.HTTP_400_BAD_REQUEST)


#project detail
class DetailProject(APIView):
  permission_classes = [IsAuthenticated, AuthUserPermission]
  authentication_classes = [TokenAuthentication]

  def get (self, request, id):
    try:
      project = models.Project.objects.get(id = id)
      
      self.check_object_permissions(request, project)
      
      serializer = ProjectSerializers(project)
      
      
      return Response(serializer.data, status=status.HTTP_200_OK)
    
    except models.Project.DoesNotExist:
      context = {'error': 'could not find it'}
      return Response (context, status=status.HTTP_404_NOT_FOUND)
    

  def patch(self, request, id):
    try:
      project = models.Project.objects.get(id=id)
    except project.DoesNotExist:
      return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Handle deleted images
    try :
      if 'image1' in request.data:
        project.deleteImage1()
    except:
      pass
    
    try:
      if 'image2' in request.data:
        project.deleteImage2()
    except:
      pass
    
    serializer = ProjectSerializers(project, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()# This will update the fields automatically
      return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


#export the project as pdf
class export_project_pdf(APIView):
  
  permission_classes = [IsAuthenticated, AuthUserPermission]
  authentication_classes = [TokenAuthentication]
  
  def get(self, request, id):
    # Get the project
    try:
      project = models.Project.objects.get(id=id)
      self.check_object_permissions(request, project)
    
    except models.Project.DoesNotExist:
      context = {'error': 'could not find it'}
      return Response (context, status=status.HTTP_404_NOT_FOUND)

    #################################
    # Construct the base URL
    base_url = f"{request.scheme}://{request.get_host()}"

    # Construct absolute URLs for images
    image1_url = f'file://{os.path.join(settings.MEDIA_ROOT, project.image1.name)}' if project.image1 else None
    image2_url = f'file://{os.path.join(settings.MEDIA_ROOT, project.image2.name)}' if project.image2 else None


    
    # Render the HTML template with the project data
    html_string = render_to_string('project_app/project_template.html', {'project': project, 'image1_url':image1_url, 'image2_url':image2_url, 'req':base_url })
    
    # Create a WeasyPrint HTML object
    html = HTML(string=html_string, base_url=base_url)
    
    # Generate the PDF
    pdf = html.write_pdf()
    
    # Create an HTTP response with the PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{project.title}_export.pdf"'
    return response 
  

#for the AI request summarize

class SummarizeText(APIView):
  
  def post(self, request):
    # Get the text from the request
    text = request.data.get('text', '')

    # Hugging Face API endpoint and headers facebook
    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {
      "Authorization": f"Bearer {settings.HUGGING_FACE_API_TOKEN}",
      "x-wait-for-model": "true"  # Wait for the model to load
    }
    payload = {
      "inputs": text,
      "parameters": {
        "max_length": 130, 
        "min_length": 1,   
        "do_sample": False  
      }
    }

    try:
      # Send the request to Hugging Face
      response = requests.post(api_url, headers=headers, json=payload)
      response.raise_for_status()  # Raise an error for bad status codes
      return Response({'summurize':response.json()}, status=status.HTTP_200_OK)
    
    except requests.exceptions.RequestException as error:
      # Handle errors (e.g., network issues, API errors)
      return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#share by email
class ShareProject(APIView):
  permission_classes = [AuthUserPermission, IsAuthenticated]
  authentication_classes = [TokenAuthentication]
  
  def post(self, request):
    try:
        project = models.Project.objects.get(id=request.data.get('id'))
    except models.Project.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Project not found!'})
    
    
    if request.data.get('share') == 'description':
      email = EmailMessage(
        subject= project.title,
        body= project.description,
        from_email=settings.EMAIL_HOST_USER,
        to=[request.data.get('email')],  
      )

    #for the printed one with pdf
    else:
      email = EmailMessage(
        subject= project.title,
        body= project.description,
        from_email=settings.EMAIL_HOST_USER,
        to=[request.data.get('email')], 
      )

      # Construct the base URL
      base_url = f"{request.scheme}://{request.get_host()}"
  
      # Construct absolute URLs for images
      image1_url = f'file://{os.path.join(settings.MEDIA_ROOT, project.image1.name)}' if project.image1 else None
      image2_url = f'file://{os.path.join(settings.MEDIA_ROOT, project.image2.name)}' if project.image2 else None
      
      #generate the pdf
      # Render the HTML template with the project data
      html_string = render_to_string('project_app/project_template.html', {'project': project, 'image1_url':image1_url, 'image2_url':image2_url, 'req':base_url })
      
      # Create a WeasyPrint HTML object
      html = HTML(string=html_string, base_url=base_url)
      
      # Generate the PDF
      pdf = html.write_pdf()
      email.attach(f'{project.title}.pdf', pdf, 'application/pdf')
    
    
    try:
      email.send(fail_silently=False)
      return Response({'message': 'Email sent successfully!'}, status=status.HTTP_200_OK)
    except Exception :
      return Response({'message': f'An unexpected error occurred: contact admin for support'}, status=status.HTTP_400_BAD_REQUEST)
