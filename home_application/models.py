from django.db import models

# Create your models here.
class Script(models.Model):
    name = models.CharField(max_length=16)
    desc = models.CharField(max_length=16)
    content = models.TextField(max_length=2000)
    type = models.CharField(max_length=16)
    source = models.CharField(max_length=16)
    version = models.IntegerField()
    creator = models.CharField(max_length=20)
    created_time = models.DateTimeField(auto_now_add=True)

    def transfer(self):
        dic = {}
        dic['id'] = self.id
        dic['name'] = self.name
        dic['desc'] = self.desc
        dic['content'] = self.content
        dic['type'] = self.type
        dic['source'] = self.source
        dic['version'] = self.version
        dic['creator'] = self.creator
        dic['created_time'] = self.created_time.strftime('%Y-%m-%d %H:%M:%S')
        return dic