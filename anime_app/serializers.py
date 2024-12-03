from rest_framework import serializers
from .models import UserPreference
from .anilist_utils import AnilistClient
class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ['favorite_genres', 'watched_anime']

    def update(self, instance, validated_data):

      
        instance.favorite_genres.extend(validated_data.get('favorite_genres', []))
        instance.favorite_genres = list(set(instance.favorite_genres))
        

        instance.watched_anime.extend(validated_data.get('watched_anime', []))
        instance.watched_anime = list(set(instance.watched_anime))
        
        instance.save()
        return instance
