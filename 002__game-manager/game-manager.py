


class Game:
    def __init__(self, title, genre, rel_year, hrs_played) -> None:
        self.title = title
        self.genre = genre
        self.rel_year = rel_year
        self.hrs_played = hrs_played
        self.rating = None

    def rate(self, score):
        self.rating = score

    def __str__(self) -> str:
        return f"name: {self.title} | genre: {self.genre} | release year: {self.rel_year} | hours played: {self.hrs_played}"

    def play(self, hours):
        self.hrs_played += hours

 
class GameManager:
    def __init__(self) -> None:
        self.games = []

    def add_game(self, title, genre, rel_year, hrs_played):
        for game in self.games:
            if game.title == title:
                print('game already exists')
                return
        self.games.append(Game(title, genre, rel_year, hrs_played))

    def show_games(self):
        for game in self.games:
            print(game)

    def find_game(self, title):
        for game in self.games:
            if game.title == title:
                return game
        return None

    def del_game(self, title):
        game = self.find_game(title)
        if game:
            self.games.remove(game)
        else:
            print('game not found')

    def upd_hrs(self, title, hours):
        game = self.find_game(title)
        if game:
            game.play(hours)
        else:
            print('game not found')

    def show_totalhrs(self):
        total = 0
        for game in self.games:
            total += game.hrs_played
        return total    
    def most_played(self):
        most_played_game = None
        if not self.games:
            return None
        most_played_game = self.games[0]
        for game in self.games:
            if game.hrs_played > most_played_game.hrs_played:
                most_played_game = game
        return most_played_game

    def rate_game(self, title, score):
        game = self.find_game(title)
        if game:
            game.rate(score)
        else:
            print("game not found")
