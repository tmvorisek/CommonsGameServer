from sqlalchemy import (Table, Column, select, insert, update, create_engine,
                        Integer, String, Sequence, MetaData)

metadata = MetaData()


class DBManager():
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:pass123@localhost/commons')
        self.engine.connect()
        self.game_table = Table("game", metadata,
            Column("id", Integer, Sequence("game_id_seq"), primary_key=True, nullable=False, unique=True),
            Column("resource", Integer))
        self.round_table = Table("round", metadata,
            Column("id", Integer, Sequence("round_id_seq"), primary_key=True, nullable=False, unique=True),
            Column("commons_index", Integer),
            Column("game_id", Integer))
        self.player_table = Table("player", metadata,
            Column("id", Integer, Sequence("player_id_seq"), primary_key=True, nullable=False, unique=True),
            Column("round_id", Integer),
            Column("name", String),
            Column("worth", Integer),
            Column("password", String))
        print("hey man")


    def create_games(self, games_arr):
        for game in games_arr:
            self.game_table.insert().values(resource=100)
            self.engine.execute(self.game_table.select()).fetchall()

            for player in range(0,game):

                pass

