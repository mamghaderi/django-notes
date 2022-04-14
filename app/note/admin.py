from django.contrib import admin

from note.models import Note, Tag


class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    list_display = ('id', 'title', 'body', 'public', 'owner')


class TagAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    list_display = ('id', 'name')


admin.site.register(Note, NoteAdmin)
admin.site.register(Tag, TagAdmin)
