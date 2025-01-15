from rest_framework import serializers
from ..models import Project

class ProjectSerializers(serializers.ModelSerializer):
  
  user = serializers.StringRelatedField(read_only=True)
  
  class Meta:
    model = Project
    fields = '__all__'