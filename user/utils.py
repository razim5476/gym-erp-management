"""
User utils.
"""


from django.core.mail import send_mail


def send_credentials_mail_to_member(company_name, first_name, username, temp_password, member_email):
    """
    Send mail to the member about username and password.
    """

    subject = f"Welcome to {company_name} - Your Login Credentials"

    message = f"""

                Hi {first_name},

                Welcome! Your membership has been created successfully.filter

                Here are your login credentials:


                Username : {username}
                Password : {temp_password}

                Please log in and change your password immediately.


                Regards {company_name} Team """.strip()
    

    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[member_email],
        fail_silently=False
    )


    
