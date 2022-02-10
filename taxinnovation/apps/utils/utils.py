import datetime

from django.utils.text import slugify


def unique_slug_generator(model_instance, title, slug_field):
    """
    Slug generator.

    :param model_instance:
    :param title:
    :param slug_field:
    :return:
    """
    slug = slugify(title)
    model_class = model_instance.__class__

    # noinspection PyProtectedMember
    while model_class._default_manager.filter(slug=slug).exists():
        # noinspection PyProtectedMember
        object_pk = model_class._default_manager.latest('pk').pk
        object_pk = object_pk + 1
        slug = '{}-{}'.format(slug, object_pk)
    return slug


def years_list(count_years):
    """
    Returns a list of years
    :param count_years: total years to count in the list
    :return: Years list
    """

    year_choices = []

    for r in range(1980, (datetime.datetime.now().year + 1)):
        year_choices.append((r, r))
    return year_choices
