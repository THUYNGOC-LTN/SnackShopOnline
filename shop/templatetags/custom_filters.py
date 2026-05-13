from django import template

register = template.Library()

@register.filter
def vnd(value):

    try:
        value = float(value)

        # format: 28000 -> 28,000
        formatted = "{:,.0f}".format(value)

        # đổi dấu phẩy thành dấu chấm
        formatted = formatted.replace(",", ".")

        return f"{formatted}đ"

    except:
        return value