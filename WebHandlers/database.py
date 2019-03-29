from sqlalchemy import (Table, Column, select, insert, update, create_engine,
                        Integer, String, Sequence, MetaData)

metadata = MetaData()


class DBManager():
    def __init__(self):
        self.connect("postgres","pass123","commons")

    def create_games(self, games_arr):
        for player_count in games_arr:
            game_table = self.meta.tables['game']
            self.con.execute(game_table.insert().values(resource=100))
            # self.engine.execute(game_table.select()).fetchall()

            for player in range(0,player_count):
                pass

    def connect(self, user, password, db, host='localhost', port=5432):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)

        self.con = create_engine(url, client_encoding='utf8')

        self.meta = MetaData(bind=self.con, reflect=True)


