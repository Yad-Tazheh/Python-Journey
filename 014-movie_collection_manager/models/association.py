from sqlalchemy import Table, Column, Integer, ForeignKey

from database.base import Base


movie_genres = Table(
    "movie_genres",
    Base.metadata,

    Column(""
           "movie_id",
           Integer,
           ForeignKey("movies.movie_id"),
           primary_key=True),

    Column(""
           "genre_id",
           Integer,
           ForeignKey("genres.genre_id"),
           primary_key=True
           )

)

movie_actors = Table(
    "movie_actors",
    Base.metadata,

    Column(""
           "movie_id",
           Integer,
           ForeignKey("movies.movie_id"),
           primary_key=True
           ),

    Column(""
           "actor_id",
           Integer,
           ForeignKey("actors.actor_id"),
           primary_key=True
           )
)