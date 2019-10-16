from django.db import models

# Create your models here.
class Test(models.Model):
    biz_id = models.CharField(max_length=50)
    ip = models.CharField(max_length=50)
    content = models.TextField(max_length=2000)
    cloud_id = models.CharField(max_length=50)
    creator = models.CharField(max_length=20)
    created_time = models.DateTimeField(auto_now_add=True)

    def transfer(self):
        dic = {}
        dic['id'] = self.id
        dic['biz_id'] = self.biz_id
        dic['ip'] = self.ip
        dic['content'] = self.content
        dic['cloud_id'] = self.cloud_id
        dic['creator'] = self.creator
        dic['created_time'] = self.created_time.strftime('%Y-%m-%d %H:%M:%S')
        return dic

