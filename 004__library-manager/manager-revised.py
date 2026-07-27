import uuid


class Book:
    def __init__(self, title: str, author: str, year: int) -> None:
        self.title = title
        self.author = author
        self.year = year
        self.borrowed_by = None

    @property
    def is_borrowed(self):
        return self.borrowed_by is not None

    def __str__(self) -> str:
        if self.is_borrowed:
            return f"{self.title} | {self.author} | {self.year} | Borrowed by {self.borrowed_by.name}"
        
        return f"{self.title} | {self.author} | {self.year} | Available"


class Member:
    def __init__(self, name: str) -> None:
        self.name = name
        self.id = str(uuid.uuid4())
        self.books = []

    def borrow(self, book: Book):
        self.books.append(book)

    def return_book(self, book: Book):
        self.books.remove(book)

    def __str__(self):
        return f"{self.name} | {self.id}"


class Library:
    def __init__(self) -> None:
        self.books = []
        self.members = []


    def add_book(self, book: Book):
        self.books.append(book)


    def add_member(self, member: Member):
        self.members.append(member)


    def find_book(self, title: str) -> Book | None:
        for book in self.books:
            if book.title == title:
                return book
        return None


    def find_member(self, member_id: str) -> Member | None:
        for member in self.members:
            if member.id == member_id:
                return member
        return None


    def borrow_book(self, title: str, member_id: str):

        book = self.find_book(title)
        if book is None:
            print("book not found")
            return

        member = self.find_member(member_id)
        if member is None:
            print("member not found")
            return

        if book.is_borrowed:
            print(f"book already borrowed by {book.borrowed_by}")
            return

        book.borrowed_by = member
        member.borrow(book)


    def return_book(self, title: str, member_id: str):

        book = self.find_book(title)
        if book is None:
            print("book not found")
            return

        member = self.find_member(member_id)
        if member is None:
            print("member not found")
            return

        if book not in member.books:
            print("this member doesn't have this book")
            return

        member.return_book(book)
        book.borrowed_by = None


    def show_books(self):
        for book in self.books:
            print(book)


    def show_members(self):
        for member in self.members:
            print(member)
