from django.db import models

class Task(models.Model):
    input_file = models.FileField()
    progress = models.FloatField(default=0, blank=True)

    def progress_percent(self):
        return str(round(self.progress * 100)) + '%'