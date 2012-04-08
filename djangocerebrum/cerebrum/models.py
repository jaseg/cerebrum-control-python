
class Event(models.Model):
    target = models.IntegerField()
    description = models.TextField()

    def __unicode__(self):
        return self.description
