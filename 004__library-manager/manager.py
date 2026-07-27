import uuid



class Book:
    def __init__(self, title, author, year) -> None:
        self.title = title
        self.author = author
        self.year = year
        self.is_borrowed = False
        self.borrowed_by = None

    def __str__(self) -> str:
        if self.is_borrowed:
          return f'{self.title}|{self.author}|{self.year}| Borrowed by {self.borrowed_by}'
        return f'{self.title}|{self.author}|{self.year}| Available'


class Member:
    def __init__(self, name, member_id) -> None:
        self.name = name 
        self.member_id = member_id
        self.borrowed_books = []
        
    def show_borrowed_books(self):
        return self.borrowed_books

    def __str__(self) -> str:
        return f"name: {self.name} member_id: {self.member_id}"

#    @borrowed_books.setter
#    def borrowed_books(self, book):
#        self._borrowed_books.append(book)
#
class LibMgmt:
    def __init__(self) -> None:
        self.books = []
        self.members = []


    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                    return book
        return None

    def add_book(self, title, author, year):
        book = self.find_book(title)
        if not book:
            self.books.append(Book(title, author, year))
        else:
            return book

    def find_member(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None
            
    def register_member(self, name):
        member = Member(name, str(uuid.uuid4()))
        self.members.append(member)
        return member

    def borrow_book(self, title, member_id):
        member = self.find_member(member_id)
        if member is None:
            print('member does not exists')
            return
        book = self.find_book(title)
        if book is None:
            print('book does not exists')
            return
        elif book.is_borrowed:
            print(f'book already borrowed by {book.borrowed_by}')
        else:
            book.is_borrowed = True
            member.borrowed_books.append(book)
            book.borrowed_by = member
               
    def return_book(self,title, member_id):
        member = self.find_member(member_id)
        if member is None:
            print('not a member')
            return
        book = self.find_book(title)
        if book is None:
            print('book doesnt belong here')
            return
        else:
            if book in member.borrowed_books:
                book.is_borrowed = False
                book.borrowed_by = None
                member.borrowed_books.remove(book)
            else:
                print('member didnt get this book')




    def show_books(self):
        for book in self.books:
            print(book)



    def delete_book(self, title):
        book = self.find_book(title)
        if book is None:
            print('book does not exists')
            return
        if book.is_borrowed:
            print('cant delete borrowed book')
            return
        self.books.remove(book)
    
    def show_members(self):
        for member in self.members:
            print(member)

