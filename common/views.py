from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.sites.models import Site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from projects.models import Project
from blogs.models import Blog, Comment, Reply
from .models import CustomerReview, DashboardImage, CustomerMessage
from financehouse.glob_params import HOME_VIDEO_URL, EMAIL_CUSTOMER_MESSAGES_RECEPTION_LIST, ADMIN_FACEBOOK_ID, ADMIN_TWITTER_ID, ADMIN_INSTAGRAM_ID
from .utils import send_html_mail
from .tokens import emailVerificationToken
from news.models import NewsArticle, NewsletterSubscriber
from blogs.models import Blog
from datetime import datetime

HOME_DASHBOARD_IMAGES_COUNT = 5
HOME_LATEST_PROJECTS_COUNT = 3
HOME_CUST_REVIEWS_COUNT = 15
HOME_LATEST_NEWS_ARTICLES_COUNT = 3
HOME_LATEST_BLOGS_COUNT = 3

def home(request):
    dashboard_images = DashboardImage.objects.all()[:HOME_DASHBOARD_IMAGES_COUNT]    
    latest_projects = Project.objects.all()[:HOME_LATEST_PROJECTS_COUNT]    
    customer_reviews = CustomerReview.objects.all()[:HOME_CUST_REVIEWS_COUNT]    
    latest_news_articles = NewsArticle.objects.all()[:HOME_LATEST_NEWS_ARTICLES_COUNT]    
    latest_blogs = Blog.objects.all()[:HOME_LATEST_BLOGS_COUNT]    
    context = {
        'home_video_url': HOME_VIDEO_URL,
        'dashboard_images': dashboard_images,
        'latest_projects': latest_projects,
        'customer_reviews': customer_reviews,
        'latest_news_articles': latest_news_articles,
        'latest_blogs': latest_blogs,
    }
    return render(request, 'common/home.html', context)

def about(request):    
    customer_reviews = CustomerReview.objects.all()[:HOME_CUST_REVIEWS_COUNT]    
    context = {
        'customer_reviews': customer_reviews,
    }
    return render(request, 'common/about.html', context)

def solutions(request):    
    context = {}
    return render(request, 'common/solutions.html', context)

def contact(request):    
    context = {}
    return render(request, 'common/contact.html', context)

def privacy(request):    
    context = {}
    return render(request, 'common/privacy.html', context)

def schedule_meeting(request):    
    context = {}
    return render(request, 'common/schedule-meeting.html', context)

# api calls

def createComment_AJAX(request):
    if not (request.method == "POST" and request.is_ajax()):
        return JsonResponse({'message': f'Not authorized'})
    blog_id = request.POST['blog_id']
    if blog_id is None or blog_id == "":
        return JsonResponse({'message': f'Invalid Data'})
    try:
        blog = Blog.objects.get(id=int(blog_id))
    except Blog.DoesNotExist:
        return JsonResponse({'message': f'Blog does not exist'})
    content = request.POST['content']
    if content is None or content == "" or len(content) > 500:
        return JsonResponse({'message': f'Invalid content'})
    if request.user.is_authenticated:
        comment = Comment(blog=blog, user=request.user, content=content)
        comment.save()
        message = "Successfully added Comment"
        data = {
            "added": True,
            "message": message,
            "comment_html": render_to_string('blogs/comment.html', {
                'comment': comment,     
                'request': request,
            })
        }
        return JsonResponse(data)
    else:
        name = request.POST['name']
        email = request.POST['email']
        website = request.POST['website']
        if name is None or name == "" or len(name) > 50:
            return JsonResponse({'message': f'Invalid name'})
        if email is None or email == "" or len(email) > 50:
            return JsonResponse({'message': f'Invalid email'})
        try:
            validate_email(email)
        except ValidationError as e:
            return JsonResponse({'message': f'Invalid email'})
        if len(website) > 50:
            return JsonResponse({'message': f'Invalid website'})
        comment = Comment(blog=blog, name=name, email=email, website=website, content=content)
        comment.save()
        message = "Successfully added Comment"
        data = {
            "added": True,
            "message": message,
            "comment_html": render_to_string('blogs/comment.html', {
                'comment': comment,     
                'request': request,
            })
        }
        return JsonResponse(data)

def createReply_AJAX(request):
    if not (request.method == "POST" and request.is_ajax()):
        return JsonResponse({'message': f'Not authorized'})
    comment_id = request.POST['comment_id']
    if comment_id is None or comment_id == "":
        return JsonResponse({'message': f'Invalid Data'})
    try:
        comment = Comment.objects.get(id=int(comment_id))
    except Comment.DoesNotExist:
        return JsonResponse({'message': f'Comment does not exist'})
    content = request.POST['content']
    if content is None or content == "" or len(content) > 500:
        return JsonResponse({'message': f'Invalid content.'})
    if request.user.is_authenticated:
        reply = Reply(comment=comment, user=request.user, content=content)
        reply.save()
        message = "Successfully added Reply"
        data = {
            "added": True,
            "message": message,
            "reply_html": render_to_string('blogs/reply.html', {
                'reply': reply,   
                'request': request,  
            })
        }
        return JsonResponse(data)
    else:
        name = request.POST['name']
        if name is None or name == "" or len(name) > 50:
            return JsonResponse({'message': f'Invalid name'})
        reply = Reply(comment=comment, name=name, content=content)
        reply.save()
        message = "Successfully added Reply"
        data = {
            "added": True,
            "message": message,
            "reply_html": render_to_string('blogs/reply.html', {
                'reply': reply,     
                'request': request,
            })
        }
        return JsonResponse(data)

@login_required
def deleteComment_AJAX(request):
    if not (request.method == "POST" and request.is_ajax() and request.user.is_authenticated):
        return JsonResponse({'message': f'Not authorized'})
    if not request.user.is_staff:
        return JsonResponse({'message': f'Not authorized'})
    comment_id = request.POST['comment_id']
    if comment_id is None or comment_id == "":
        return JsonResponse({'message': f'Invalid Data'})
    try:
        comment = Comment.objects.get(id=int(comment_id))
    except Comment.DoesNotExist:
        return JsonResponse({'message': f'Comment does not exist'})
    comment.delete()
    data = {
        "deleted": True,
        "message": 'Comment deleted',
    }
    return JsonResponse(data)

@login_required
def deleteReply_AJAX(request):
    if not (request.method == "POST" and request.is_ajax() and request.user.is_authenticated):
        return JsonResponse({'message': f'Not authorized'})
    if not request.user.is_staff:
        return JsonResponse({'message': f'Not authorized'})
    reply_id = request.POST['reply_id']
    if reply_id is None or reply_id == "":
        return JsonResponse({'message': f'Invalid Data'})
    try:
        reply = Reply.objects.get(id=int(reply_id))
    except Reply.DoesNotExist:
        return JsonResponse({'message': f'Reply does not exist'})
    reply.delete()
    data = {
        "deleted": True,
        "message": 'Reply deleted',
    }
    return JsonResponse(data)

def sendMessage_AJAX(request):
    if not (request.method == "POST" and request.is_ajax()):
        return JsonResponse({'message': f'Not authorized'})
    name = request.POST['name']
    email = request.POST['email']
    subject = request.POST['subject']
    message = request.POST['message']
    if name is None or name == "" or len(name) > 50:
        return JsonResponse({'message': f'Invalid name'})
    if email is None or email == "" or len(email) > 100:
        return JsonResponse({'message': f'Invalid email'})
    try:
        validate_email(email)
    except ValidationError as e:
        return JsonResponse({'message': f'Invalid email'})
    if subject is None or subject == "" or len(subject) > 150:
        return JsonResponse({'message': f'Invalid subject'})
    if message is None or message == "" or len(message) > 5000:
        return JsonResponse({'message': f'Invalid message'})
    cust_message = CustomerMessage(name=name, email=email, subject=subject, message=message)
    cust_message.save()
    data = {
        "sent": True,
        "message": 'Message successfully sent',
    }
    # schedule email to admin
    html_message = render_to_string('common/customer-message.html', {
        'name': cust_message.name,
        'email': cust_message.email,
        'subject': cust_message.subject,
        'message': cust_message.message,
        'domain': Site.objects.get_current().domain,
    }) 
    send_html_mail(cust_message.subject, html_message, EMAIL_CUSTOMER_MESSAGES_RECEPTION_LIST)
    return JsonResponse(data)
    
def newsletterSubscribe_AJAX(request):
    if not (request.method == "POST" and request.is_ajax()):
        return JsonResponse({'message': f'Not authorized'})
    email = request.POST['email']
    if email is None or email == "" or len(email) > 100:
        return JsonResponse({'message': f'Invalid email'})
    email = email.strip(' ').lower()
    try:
        validate_email(email)
    except ValidationError as e:
        return JsonResponse({'message': f'Invalid email'})
    try:
        subscriber = NewsletterSubscriber.objects.get(email=email)
    except NewsletterSubscriber.DoesNotExist:
        subscriber = NewsletterSubscriber(email=email)
        subscriber.save()
        data = {
            "added": True,
            "message": 'You are now subscribed to our Newsletter!',
        }
        # schedule email to new subscriber
        html_message = render_to_string('news/subscriber-welcome.html', {
            'name': subscriber.email.split("@")[0],
            'email': subscriber.email,
            'domain': Site.objects.get_current().domain,
            'id_facebook': ADMIN_FACEBOOK_ID,
            'id_twitter': ADMIN_TWITTER_ID,
            'id_instagram': ADMIN_INSTAGRAM_ID,
            'todays_date': datetime.today(),
            'uid': urlsafe_base64_encode(force_bytes(subscriber.pk)),
            'token': emailVerificationToken.make_token(subscriber),
        }) 
        subject = 'Welcome to Our Newsletter Subscription'
        send_html_mail(subject, html_message, [subscriber.email])
        return JsonResponse(data)
    return JsonResponse({'message': f'You are already subscribed to our Newsletter'})

def newsletterUnsubscribe(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        sub2 = NewsletterSubscriber.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, NewsletterSubscriber.DoesNotExist):
        sub2 = None
    if sub2 is not None and emailVerificationToken.check_token(sub2, token):
        sub2.delete()
        status = 'Unsubscribed'
        message = 'You are successfully unsubscribed from our Newsletter'
    else:
        status = 'Error!'
        message = 'Invalid action'
    context = {
        'status': status,
        'message': message,
    }
    return render(request, 'news/unsubscribed.html', context)

# sched newsletter task
from .tasks import schedule_newsletter
schedule_newsletter()