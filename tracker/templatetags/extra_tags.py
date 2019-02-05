from django import template

from tracker.models import *

register = template.Library()

@register.simple_tag
def is_employee(username):
    try:
        emp = Employee.objects.get(email=username).exclude(status='Delete')
        return True
    except Exception as inst:
        return False