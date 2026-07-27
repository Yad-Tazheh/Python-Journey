
operations_menu = """
1 Add movie
2 Show movies
3 Find movies
4 Delete movie
5 Update movie year
6 Exit
"""


class Movie:
    def __init__(self, title, director, year) -> None:
        self.title = title
        self.director = director 
        self.year = year

    def __str__(self) -> str:
        return f"name: {self.title} | director: {self.director} | year: {self.year}"

class MovieManager:
    def __init__(self) -> None:
        self.movies = []


    def add_movie(self, title, director, year):
        for movie in self.movies:
            if movie.title == title:
                print('movie in the list')
                return
        self.movies.append(Movie(title, director, year))
    
    def show_movies(self):
        if not self.movies:
            print('no movies available')
            return 
        for movie in self.movies:
            print(movie)

    def find_movie(self, title):
        for movie in self.movies:
            if movie.title == title:
                return movie
        return None

    def delete_movie(self, title):
        title = self.find_movie(title)
        if title in self.movies:
            self.movies.remove(title)
            print('movie deleted')
        else:
            print('movie not found')

    def update_year(self, title, year):
        movie = self.find_movie(title)
        if movie:
            movie.year = year
        else:
            print('movie not found')










