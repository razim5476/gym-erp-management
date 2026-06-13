"""
Helper fucntiions
"""

import random
import string

from core.models import UniqueId
import logging



error_logger = logging.getLogger(__name__)



def generate_unique_id(model_name, string, branch):
    """
    Return unique id per branch by per model.
    """

    try:

        unique_id = UniqueId.objects.filter(
            model=model_name,
            prefix=string,
            branch=branch
        ).first()

        if unique_id != None:

            prefix = unique_id.prefix
            unique_id = unique_id.unique_id
            new_unique_id = unique_id + 1
            prefix_and_unique_id = f"{prefix}{new_unique_id}"

            return prefix_and_unique_id

        else:

            unique_id_obj = UniqueId.objects.create(
                model=model_name,
                branch=branch,
                prefix=string
            )

            return f"{unique_id_obj.prefix}{unique_id_obj.unique_id}"
        

    except Exception as e:
        error_logger.error(f"Unique id generation failed: {str(e)}")

        
def generate_id():
    """
    Unique id generation for company and branch
    """

    id = random.randint(1000, 1000000000)
    char = random.choice(string.ascii_letters)

    return "VELOCITY-{id}-{char}"


