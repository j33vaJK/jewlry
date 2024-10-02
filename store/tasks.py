# # Create tasks that will be executed periodically.


# from celery import shared_task
# from django.core.mail import send_mail
# from .models import MessageTemplate
# from .utils import send_sms

# @shared_task
# def send_periodic_messages():
#     # Example task: Send a message to all users about a seasonal offer
#     template = MessageTemplate.objects.filter(title="Seasonal Offer", is_active=True).first()
    
#     if template:
#         users = User.objects.all()  # Adjust this to target specific users
#         for user in users:
#             send_sms(user, template)


# from celery import shared_task
from .utils import send_sms

# @shared_task
def send_promotional_sms():
    phone_numbers = [8129907709]  # Replace with actual user phone numbers
    message = "Check out our new arrivals and discounts!"
    
    response = send_sms(message, phone_numbers)
    return response
