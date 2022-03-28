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
