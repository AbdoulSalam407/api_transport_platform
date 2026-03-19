"""
Utilitaires et helpers
"""
import uuid
from django.utils.text import slugify


def generate_transaction_reference():
    """Générer une référence de transaction unique"""
    return f"TXN-{uuid.uuid4().hex[:12].upper()}"


def format_phone_number(phone):
    """Formater un numéro de téléphone"""
    return phone.replace(" ", "").replace("-", "")
