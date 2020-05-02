from django import template

register = template.Library()

@register.filter
def get_page_list(items):
    max_page_items = 9
    pages = []

    current = items.number
    num_pages = items.paginator.num_pages

    if num_pages == 1:
        return pages

    start = max(1, current - max_page_items // 2)
    end  = start + max_page_items - 1

    if end > num_pages:
        start = max(1, start - (end - num_pages))
        end = num_pages

    for i in range(start, end+1):
        pages.append(i)

    return pages



@register.filter
def has_discounted_price(item):
    if item.discounted_price == item.price:
        return False
    else:
        return True



@register.filter
def get_stock_range(product):

    return range(1, min(10, product.stock) + 1)



@register.filter
def get_subtotal_price(basket_item):

    return basket_item.product.price * basket_item.quantity
