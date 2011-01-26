from django.contrib.auth.decorators import login_required
from django.contrib.comments.models import Comment
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
import logging
import settings

@login_required
def delete(request, comment_id):
    try:
        comment = Comment.objects.get( pk=comment_id,
                                       site__pk=settings.SITE_ID )

        if comment.user == request.user or request.user.is_staff:
            logging.info( 'removing comment ' + str(comment_id) )
            comment.is_removed = True
            comment.save()
        else:
            logging.warning( str(request.user) + ' trying to delete comment ' + str(comment_id) + ' of ' + str(comment.user) )
    except ObjectDoesNotExist:
        logging.warning( "Trying to delete comment which doesnt exist: " + str(comment_id) )
        
    return redirect( get_redirect_target(request) )

def get_redirect_target(request):
    if 'next' in request.GET:
        next = request.GET['next']
    else:
        next = '/'
    return next
