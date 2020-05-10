from django.db.models.signals import post_save

import notifications.notify

from blog.models import Posts


# def my_handler(sender, instance, created, **kwargs):
#     notify.send(instance, verb='was saved')
#
# post_save.connect(my_handler, sender=Posts)