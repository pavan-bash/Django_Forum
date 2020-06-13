from django.contrib import admin
from .models import *

admin.site.register(Community)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(CommunityJoin)
admin.site.register(ReportQ)
admin.site.register(ReportA)
admin.site.register(Tag)
admin.site.register(ReplyAnswer)
