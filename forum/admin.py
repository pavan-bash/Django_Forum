from django.contrib import admin
from .models import *

admin.site.register(Community)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(CommunityJoin)
admin.site.register(Upvote)
admin.site.register(Downvote)
