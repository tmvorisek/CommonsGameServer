from sqlalchemy import (Table, Column, select, insert, update, create_engine,
                        Integer, String, Sequence, MetaData)

metadata = MetaData()


class DBManager():
    def __init__(self):
        self.connect("postgres","pass123","commons")

    def create_games(self, games_arr):
        game_number = 1
        for player_count in games_arr:
            game_table = self.meta.tables['game']
            self.con.execute(game_table.insert().values(resource=100))
            round_table = self.meta.tables['round']
            self.con.execute(round_table.insert().values(game_id = game_number,commons_index = 2000))
            for player in range(0,player_count):
                player_table = self.meta.tables['player']
                self.con.execute(player_table.insert().values(round_id = game_number, name="bob",password="123",worth=0))
            
            game_number = game_number+1


    def connect(self, user, password, db, host='localhost', port=5432):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)
        self.con = create_engine(url, client_encoding='utf8')
        self.meta = MetaData(bind=self.con, reflect=True)

    #sends chat to data base
    def send_chat(self, msg):
        game_table = self.meta.tables['chat']
        self.con.execute(game_table.insert().values(player_id = 1,text=msg["text"], game_id=1))

    #retrieves round data from data base
    def get_round_data(self, msg):
        game_table = self.meta.tables['round']
        result = self.con.execute('SELECT * FROM '
                        '"round" where id=1')
        return result