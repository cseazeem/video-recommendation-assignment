from typing import List

def paginate(items: List, page: int = 1, page_size: int = 20):
    page = max(1, int(page))
    page_size = max(1, min(100, int(page_size)))
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end]
