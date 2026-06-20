from .models import Message

def unread_messages_count(request):
    if request.user.is_authenticated:
        # Count unread messages where the user is a participant but not the sender
        count = Message.objects.filter(thread__participants=request.user, is_read=False).exclude(sender=request.user).count()
        return {'unread_chat_count': count}
    return {'unread_chat_count': 0}
