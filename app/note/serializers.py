from rest_framework import serializers

from note.models import Note, Tag


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class TagSlugRelatedField(serializers.SlugRelatedField):

    def to_internal_value(self, data):
        return self.get_queryset().get_or_create(**{self.slug_field: data})[0]


class NoteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    tags = TagSlugRelatedField(queryset=Tag.objects.all(), many=True, required=False, slug_field='name')

    class Meta:
        model = Note
        fields = ('id', 'title', 'tags', 'body', 'public', 'owner')
        read_only_fields = ('id', 'owner')
