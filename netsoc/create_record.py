import logging
from .import models
import os

CURR_DIR=os.path.dirname(os.path.abspath(__file__))
RECORD=os.path.join(CURR_DIR,'Record')
file=os.path.join(RECORD,'records.log')

def record_store(id,type,activity):

    logging.basicConfig(filename=file,level=logging.INFO,format = '%(asctime)s %(message)s')

    if type=='post':

        instance=models.post.objects.get(pk=id)
        message=", user : {}, model : post id={}, activity : {},\n TEXT : {} ".format(instance.post_user.username,instance.id,activity,instance.post_text )


    elif type=='comment':
        instance=models.comment.objects.get(pk=id)
        message=", user : {}, model : comment id = {} : post id = {}, activity : {},\n TEXT : {} ".format(instance.comment_user.username,instance.id,instance.comment_post.id,activity,instance.comment_text )

    logging.info(message)
