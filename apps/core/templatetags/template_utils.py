from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.filter
def get_range(value):
    return range(value)


@register.filter
def page_median(from_, to_):
    return (from_ + to_) // 2


@register.filter
def multiply(arg1, arg2):
    return arg1 * arg2


@register.filter
def ab_rating_normalizer(a, b):
    # Normalize rating b to range from 0 to 50 using range between 0 and a
    return 0 if a == 0 else int(b / a * 50)
