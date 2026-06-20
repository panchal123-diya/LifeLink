from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Max
from django.http import JsonResponse
from .models import ChatThread, Message
from accounts.models import User

@login_required
def inbox(request):
    # Get all threads for the user, ordered by the latest message
    threads = ChatThread.objects.filter(participants=request.user).annotate(
        last_message_time=Max('messages__timestamp')
    ).order_by('-last_message_time')
    
    thread_data = []
    for thread in threads:
        other_user = thread.participants.exclude(id=request.user.id).first()
        last_message = thread.messages.order_by('-timestamp').first()
        unread_count = thread.messages.filter(is_read=False).exclude(sender=request.user).count()
        
        if other_user:
            thread_data.append({
                'thread': thread,
                'other_user': other_user,
                'last_message': last_message,
                'unread_count': unread_count,
            })
            
    return render(request, 'chat/inbox.html', {'thread_data': thread_data})

@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(ChatThread, id=thread_id, participants=request.user)
    other_user = thread.participants.exclude(id=request.user.id).first()
    
    # Mark messages as read
    thread.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    messages = thread.messages.order_by('timestamp')
    
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            msg = Message.objects.create(
                thread=thread,
                sender=request.user,
                text=text
            )
            # Update thread's updated_at
            thread.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'ok',
                    'message': {
                        'id': msg.id,
                        'text': msg.text,
                        'sender': msg.sender.username,
                        'timestamp': msg.timestamp.strftime("%b %d, %I:%M %p")
                    }
                })
            return redirect('thread_detail', thread_id=thread.id)
            
    return render(request, 'chat/thread.html', {
        'thread': thread,
        'other_user': other_user,
        'chat_messages': messages,
    })

@login_required
def start_chat(request, user_id):
    if request.user.id == user_id:
        return redirect('inbox')
        
    other_user = get_object_or_404(User, id=user_id)
    
    # Find existing thread
    thread = ChatThread.objects.filter(participants=request.user).filter(participants=other_user).first()
    
    if not thread:
        thread = ChatThread.objects.create()
        thread.participants.add(request.user, other_user)
        
    return redirect('thread_detail', thread_id=thread.id)
