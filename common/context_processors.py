from financehouse.glob_params import (ADMIN_FACEBOOK_ID, ADMIN_INSTAGRAM_ID, ADMIN_TWITTER_ID, 
    BASIC_INFO__COMPANY_NAME, BASIC_INFO__COMPANY_ABOUT_DASH, BASIC_INFO__COMPANY_ABOUT_FOOTER, 
    BASIC_INFO__COMPANY_TAGLINE, BASIC_INFO__CONTACT_ADDRESS,
    BASIC_INFO__CONTACT_EMAIL, BASIC_INFO__CONTACT_TELEPHONE, 
    GOOGLE_MAPS_API_KEY, GOOGLE_MAPS_LATITUDE, GOOGLE_MAPS_LONGITUDE)
from django.contrib.sites.models import Site

def social_links_processor(request):
    return {
        'social_id_facebook': ADMIN_FACEBOOK_ID,
        'social_id_twitter': ADMIN_TWITTER_ID,
        'social_id_instagram': ADMIN_INSTAGRAM_ID,
    }

def domain_name_processor(request):
    return {
        'domain': Site.objects.get_current().domain,
    }

def basic_info_processor(request):
    return {
        'basic_info_company_name': BASIC_INFO__COMPANY_NAME,
        'basic_info_company_about_dash': BASIC_INFO__COMPANY_ABOUT_DASH,
        'basic_info_company_about_footer': BASIC_INFO__COMPANY_ABOUT_FOOTER,
        'basic_info_company_tagline': BASIC_INFO__COMPANY_TAGLINE,
        'basic_info_contact_address': BASIC_INFO__CONTACT_ADDRESS,
        'basic_info_contact_telephone': BASIC_INFO__CONTACT_TELEPHONE,
        'basic_info_contact_email': BASIC_INFO__CONTACT_EMAIL,
        
        'google_maps_api_key': GOOGLE_MAPS_API_KEY,
        'google_maps_latitude': GOOGLE_MAPS_LATITUDE,
        'google_maps_longitude': GOOGLE_MAPS_LONGITUDE,
    }