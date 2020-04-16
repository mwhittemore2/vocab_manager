from ...models import Book

def create_book(doc, page_num):
    book = Book(
                title=doc["title"],
                author=doc["author"],
                language=doc["language"],
                page_number=page_num
                )
    return book