from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def pagination(object, current_page, item_per_page):
    """
    Helper function that uses django's paginator

    :param object: list or queryset object
    :param current_page: current page
    :param item_per_page: number of items we want on the page
    :return:
    """
    paginator = Paginator(object, item_per_page)

    try:
        pagination = paginator.page(current_page)
    except PageNotAnInteger:
        pagination = paginator.page(1)
    except EmptyPage:
        pagination = paginator.page(paginator.num_pages)

    return pagination
