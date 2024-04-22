from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    
    def validate_name(self, value):

        if Department.objects.filter(name=value).exists():
            raise serializers.ValidationError("Tên bộ phận đã tồn tại.")
        return value
    
    
    def create(self, validate_data):
        
        department = Department(     
            name = validate_data.get('name')
        )
        department.save()
        
        return department
    
    def create(self, validate_data):
        department = Department(
            name = validate_data.get('name')
        )
        department.save()
        return department
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
    
    def delete(self, instance):
        instance.delete()
    
    def to_representation(self, instance):
        
        representation = {
            'id': instance.id,
            'name': instance.name,
        }
        return representation
    
        
