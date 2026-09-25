"""
User module services
"""

import random
import string

from user.models import User



class UserServices:

    class MemberServices:
        """
        Services related to Members
        """

        @staticmethod
        def generate_username_for_memeber(firstname, lastname):
            """
            Generate unique username for memeber
            """

            name = f"{firstname}_{lastname}"
            suffix = ''.join(random.choices(string.digits, k=4))
            username = f"{name}_{suffix}"

            while User.objects.filter(username=username).exists():
                suffix = ''.join(random.choices(string.digits, k=4))
                username = f"{name}_{suffix}"

            return username
        

        @staticmethod
        def generate_temporary_password(company_obj, firstname, lastname):
            """
            genrate random temporray paswword.
            CMP@firstnamelastname
            """
            company_short_form = (
                company_obj.short_name
                or company_obj.name
                or "GYM"
            ) if company_obj else "GYM"
            return f'{company_short_form}@{firstname}{lastname}'


        @staticmethod
        def create_member_login_credentials(request, firstname, lastname):
            """
            Create memeber related login and credentials and passwords.
            """

            company_obj = request.user.company
            username = (
                UserServices.MemberServices.generate_username_for_memeber(
                    firstname=firstname,
                    lastname=lastname
                )
            )
            password_teemp = (
                UserServices.MemberServices.generate_temporary_password(
                    company_obj=company_obj,
                    firstname=firstname,
                    lastname=lastname
                )
            )

            return {
                "username": username,
                "temp_password": password_teemp,
            }
