import random
import string
from django.utils.text import slugify
from PIL import Image
from html.parser import HTMLParser
from datetime import datetime, date, timedelta
import time
# from io import StringIO
import threading
from threading import Thread
from django.core.mail import EmailMessage

# #####~~~~~ UTILITY CLASS ~~~~~#####
# class URLSeeker(HTMLParser):
#     def __init__(self, tag='img', attr='src'):
#         HTMLParser.__init__(self)
#         self.urls = []
#         self.tag = tag
#         self.attr = attr

#     def handle_starttag(self, tag, attrs):
#         if tag == self.tag:
#             url = dict(attrs).get(self.attr)
#             if url:
#                 self.urls.append(url)

#     def close(self):
#         super().close()
#         self.urls = []

# #####~~~~~ UTILITY CLASS ~~~~~#####
# class MLStripper(HTMLParser):
#     def __init__(self):
#         super().__init__()
#         self.reset()
#         self.strict = False
#         self.convert_charrefs= True
#         self.text = StringIO()

#     def handle_data(self, d):
#         self.text.write(d)
    
#     def get_data(self):
#         return self.text.getvalue()

# #####~~~~~ UTILITY CLASS INSTANCE ~~~~~#####
# image_url_seeker = URLSeeker('img', 'src')

# #####~~~~~ UTILITY CLASS INSTANCE ~~~~~#####
# html_tag_strip = MLStripper()

# #####~~~~~ UTILITY FUNCTION ~~~~~#####
# def stripTagsHTML(html):
#     html_tag_strip.feed(html)
#     text_data = html_tag_strip.get_data()
#     html_tag_strip.close()
#     return text_data

#####~~~~~ UTILITY FUNCTION ~~~~~#####
def resizeImage(path, x, y):
    img = Image.open(path)
    if img.height > x or img.width > y:
        output_size = (x, y)
        img.thumbnail(output_size)
        img.save(path)

#####~~~~~ UTILITY FUNCTION ~~~~~#####
def computeProminentColor(path):
    img = Image.open(path)
    colors = img.convert('RGBA').getcolors(img.size[0]*img.size[1])
    # select only colors above a certain level of transparency
    filtered_colors = list(filter(lambda x : x[1][3] > 155, colors))
    prominent_hex = '000000'    # hex black
    if len(filtered_colors) != 0:
        sorted_colors = list(sorted(filtered_colors, key=lambda x: x[0], reverse=True))
        p = sorted_colors[0]
        if p[1][3] == 255:
            prominent_hex = '%02x%02x%02x' % (round(p[1][0]), round(p[1][1]), round(p[1][2]))
        else:
            prominent_hex = '%02x%02x%02x%02x' % (round(p[1][0]), round(p[1][1]), round(p[1][2]), round(p[1][3]))
    return prominent_hex

# #####~~~~~ UTILITY FUNCTION ~~~~~#####
# def getImageLinks(html):
#     image_url_seeker.feed(html)
#     url_list = image_url_seeker.urls
#     image_url_seeker.close()
#     return url_list


def get_timesince_minified(dt):
    now = datetime.now()
    td = abs(now.replace(tzinfo=None) - dt.replace(tzinfo=None))
    days = td.days
    if days > 365:
        return str(int(days/365.0)) + 'y'
    elif days > 30:
        return str(int(days/30.0)) + 'mo'
    elif days > 0:
        return str(int(days)) + 'd'
    else:
        seconds = td.seconds
        if seconds >= 86400:
            return '1d'
        elif seconds >= 3600:
            return str(int(seconds/3600)) + 'h'
        elif seconds >= 60:
            return str(int(seconds/60)) + 'm'
        else:
            return '0m'
    return '0d'

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMessage(self.subject, self.html_content, to=self.recipient_list)
        msg.content_subtype = "html"
        msg.send()

def send_html_mail(subject, html_content, recipient_list):
    EmailThread(subject, html_content, recipient_list).start()


def get_seconds_until_next_weekday_hour(weekday_name, hour_int):
    weekday_int = time.strptime(weekday_name, "%A").tm_wday
    tod = datetime.today()
    if not (tod.weekday() == weekday_int and tod.hour < hour_int):
        tod = tod + timedelta(days=1)
        while(tod.weekday() != weekday_int):
            tod = tod + timedelta(days=1)
    sched = tod.replace(hour=hour_int, minute=0, second=0, microsecond=0)
    return int((sched - datetime.now()).total_seconds())

def get_seconds_until_next_weekday_hour_minute(weekday_name, hour_int, minute_int):
    weekday_int = time.strptime(weekday_name, "%A").tm_wday
    tod = datetime.today()
    if not (tod.weekday() == weekday_int and ((tod.hour == hour_int and tod.minute < minute_int) or (tod.hour < hour_int and tod.minute < minute_int))):
        tod = tod + timedelta(days=1)
        while(tod.weekday() != weekday_int):
            tod = tod + timedelta(days=1)
    sched = tod.replace(hour=hour_int, minute=minute_int, second=0, microsecond=0)
    return int((sched - datetime.now()).total_seconds())