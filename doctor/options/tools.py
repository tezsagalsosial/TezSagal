from time import time


def get_base_slider(instance, filename):
    return "slider/%s_%s" % (str(time()).replace('.', '_'), filename)


def get_base_blog(instance, filename):
    return "blog/%s_%s" % (str(time()).replace('.', '_'), filename)


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

PAYMENT_TYPE = (
    (1, "Nəğd"),
    (2, "Kartla")
)

MONEY_TYPE = (
    ("azn","AZN"),
    ("rub","RUB"),
    ("usd","USD"),
    ("eur","EUR"),
    ("gel","GEL"),
    ("try","TRY"),

)
