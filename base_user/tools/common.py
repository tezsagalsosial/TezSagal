from time import time
import random
import string
import calendar
from datetime import date


def get_user_profile_photo_file_name(instance, filename):
    return "profile/%s_%s" % (str(time()).replace('.', '_'), filename)


# Models Helper choices here
GENDER = (
    (1, "Kişi"),
    (2, "Qadın")
)
POSITION = (
    (1, "Fənn Müəllimi"),
    (2, "Ibtidai sinif Müəllimi")
)

USERTYPES = (
    (1, "Həkim"),
    (2, "Normal user"),
    (3, "Administrator")
)

PAYMENT_STATUS = (
    (1, "Gecikir"),
    (2, "Normal"),
    (3, "Vaxtinda")
)

ATTENDANCE = (
    (1, "plus"),
    (2, "minus"),
    (3, "icazəli"),
    (4, "çıxıb"),
)


# Custom slugify function
def slugify(title):
    symbol_mapping = (
        (' ', '-'),
        ('.', '-'),
        (',', '-'),
        ('!', '-'),
        ('?', '-'),
        ("'", '-'),
        ('"', '-'),
        ('ə', 'e'),
        ('ı', 'i'),
        ('ö', 'o'),
        ('ğ', 'g'),
        ('ü', 'u'),
        ('ş', 's'),
        ('ç', 'c'),
    )

    title_url = title.strip().lower()

    for before, after in symbol_mapping:
        title_url = title_url.replace(before, after)

    return title_url


confirmation_link = "http://%s/az/account/confirmation/?code=%s&csrfmiddlewaretoken=yqblx5XHw9E57i1UVPktCXWGWGYaFiV92o8EifbH2lZ3rMNJdphusTdxZO6AMLC8&user=%s"
forget_link = "http://%s/az/account/forget/?code=%s&csrfmiddlewaretoken=yqblx5XHw9E57i1UVPktCXWGWGYaFiV92o8EifbH2lZ3rMNJdphusTdxZO6AMLC8"

def id_generator(size=120, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def change_pass(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
