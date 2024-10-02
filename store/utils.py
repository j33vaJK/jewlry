import requests
from .models import Profile  # Import Profile model



def fetch_phone_numbers():
    phone_numbers = Profile.objects.exclude(phone_number__isnull=True).values_list('phone_number', flat=True)
    return list(phone_numbers)
    

def send_whatsapp_message(apikey, mobile_numbers, text_message=None, image_url=None):
    
    url = "http://api.whatsappmessages.in/wapp/api/send"
    print('calling send whatsapp')
    # Ensure mobile_numbers is a list
    if isinstance(mobile_numbers, str):
        mobile_numbers = [mobile_numbers]

    data = {
        'apikey': apikey,
        'mobile': ','.join(mobile_numbers),
        'msg': text_message or ""

    }

    # # Check if an image is included
    # if image_url:
    
    data['img1'] = image_url  # Or use the parameter name required by the API
    
    try:
        # Use POST method if API requires it for media
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print('success')
            return f"Message sent successfully: {response.text}"
        else:
            return f"Failed to send message: {response.status_code}, {response.text}"
    except Exception as e:
    
        return f"An error occurred: {e}"


def send_registration_message(apikey, user_phone_number, user_name):
    message = f"Hello {user_name},\n\nWelcome to Subbiah Jewellery ✨\n\n We’re delighted to have you here! At Subbiah Jewellery, we celebrate beauty and craftsmanship with our exquisite collection of fine jewelry, designed to add a sparkle to every moment.\n Whether you're searching for timeless elegance or modern, fancy designs, we are here to offer you the perfect piece that tells your story."

    # Call the WhatsApp message sending function
    result = send_whatsapp_message(apikey, [user_phone_number], message)
 
    return result