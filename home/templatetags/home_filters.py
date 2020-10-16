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
def pagination(news):
    pages_number=[]
    num_pages=news.paginator.num_pages
    current=news.number

    if num_pages<10:
        return [i for i in news.paginator.page_range]

    elif num_pages > 10:
        if (current<=3):
            pages_number=[num for num in range(1,current+2)]
            if num_pages > 5:
                pages_number += ['...',num_pages-1,num_pages]
            return pages_number 
        elif (current>3 and current<=int(num_pages/2)):

            pages_number=[num for num in range(current-1,current+3)]
            pages_number=[1,'...']+pages_number+["...",num_pages-2,num_pages-1,num_pages]

            return pages_number
        else:
            pages_number=[num for num in range(int(num_pages/2),num_pages+1)]
            pages_number=[1,"..."]+pages_number
            return pages_number
         