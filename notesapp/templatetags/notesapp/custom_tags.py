from django import template
from random import choice


register = template.Library()


def rand_card_bg():
    bg_classes = [
        'bg-info',
        'bg-primary',
        'bg-secondary',
        'bg-danger',
        'bg-warning',
        'bg-success',
        'bg-dark'
    ]
    rand_bg = choice(bg_classes)
    return rand_bg


register.simple_tag(name='random_card_background', func=rand_card_bg)
