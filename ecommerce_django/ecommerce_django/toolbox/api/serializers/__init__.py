from django.core.paginator import Paginator


class Pagination:

    per_page = 30

    def __init__(self, items, per_page=None):
        if per_page is not None:
            self.per_page = per_page
        self.paginator = Paginator(items, self.per_page)
        self.num_pages = self.paginator.num_pages

    def get_items(self, page):
        if page > self.num_pages:
            return []
        return self.paginator.page(page).object_list
