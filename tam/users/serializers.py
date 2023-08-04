from rest_framework import serializers
from .models import Profile


class ProfileTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'id']



class ProfileSerializer(serializers.ModelSerializer):
    profile_image =serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Profile
        exclude = ['created']
        
    def get_image_url(self, obj):
        image_url = obj.profile_image.url
        image_url = image_url[1:]
        return image_url