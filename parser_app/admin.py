from django.contrib import admin
from .models import Resume
from .models import job
from .models import applicants
from .models import contactComment
from .models import recruiters

@admin.register(Resume)
@admin.register(applicants)
class ResumeAdmin(admin.ModelAdmin):
    pass
admin.site.register(job)
admin.site.register(recruiters)