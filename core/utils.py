"""
Helper fucntiions
"""

import random
import string

from django.db import transaction

from core.models import UniqueId
import logging



error_logger = logging.getLogger(__name__)



def generate_unique_id(model_name, string, branch, created_by=None):
    """
    Return unique id per branch by per model.
    """

    try:
        with transaction.atomic():
            unique_id_obj = UniqueId.objects.select_for_update().filter(
                model=model_name,
                prefix=string,
                branch_id=branch
            ).first()

            if unique_id_obj is None:
                unique_id_obj = UniqueId.objects.create(
                    model=model_name,
                    branch_id=branch,
                    prefix=string,
                    unique_id=1,
                    created_by=created_by or 1
                )
                return f"{unique_id_obj.prefix}{unique_id_obj.unique_id}"

            unique_id_obj.unique_id += 1
            unique_id_obj.save(update_fields=["unique_id", "updated_at"])

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
