from sqlalchemy import (Table, Column, select, insert, update, create_engine,
                        Integer, String, Sequence, MetaData, func)
import uuid

metadata = MetaData()


class DBManager():
    def __init__(self):
        self.connect("postgres","pass123","commons")

    def get_move_num(self, player_id):
        move_table = self.meta.tables['move']
        moves = move_table.select().where(
            move_table.c.player_id == player_id).execute().fetchall()

    def store_move(self, player_id, game_id, move):
        move_table = self.meta.tables['move']
        move_table.insert().values(
            player_id=player_id,
            game_id=game_id,
            harvest=move).execute()


    def get_chats(self, round_id, game_id):
        chat_table = self.meta.tables['chat']
        player_table = self.meta.tables['player']
        round_table = self.meta.tables['round']
        rounds = round_table.select().where(
            round_table.c.game_id == game_id).where(
            round_table.c.id <= round_id).execute().fetchall()
        chat_log = []
        for r in rounds:
            chat_log.append(chat_table.join(player_table, 
                chat_table.c.player_id == player_table.c.id).select(
                chat_table.c.round_id == r[2]).execute().fetchall())
        return chat_log


    def store_chat(self, obj):
        chat_table = self.meta.tables['chat']
        chat_table.insert().values(
            player_id=obj['player_id'],
            text=obj['text'],
            round_id=obj['round_id']).execute()


    def set_name(self, player_id, name_string):
        player_table = self.meta.tables['player']
        player_table.update().values(name=name_string).where(
            player_table.c.id==player_id).execute()

    def check_pass(self, pass_string):
        player_table = self.meta.tables['player']
        player = player_table.select().where(
            player_table.c.password==pass_string).execute().fetchone()
        if(player!=None):
            return player[0]
        return False

    def get_player_details(self, player_id):
        player_table = self.meta.tables['player']
        round_table = self.meta.tables['round']
        move_table = self.meta.tables['move']
        player_details = player_table.select().where(
            player_table.c.id==player_id).execute().fetchone()
        round_details = round_table.select().where(
            round_table.c.id==player_details[1]).execute().fetchone()
        move_details = move_table.select().where(
            move_table.c.player_id == player_id).execute().fetchall()
        other_players = select([player_table.c.id,player_table.c.name]).where(
            player_table.c.round_id.in_(select([round_table.c.id]).where(
                round_table.c.game_id == round_details[2]))).execute().fetchall()
        print(other_players)


        return {"player_id":player_details[0],
                "game_id":round_details[2],
                "move_num":len(move_details),
                "round_id":player_details[1],
                "name":player_details[2],
                "worth":player_details[3],
                "other_players":other_players,
                "type":"connection"}

    def load_games(self):
        game_table = self.meta.tables['game']
        round_table = self.meta.tables['round']
        player_table = self.meta.tables['player']
        games_list = {}

        for g in select([game_table.c.id]).execute().fetchall():
            rounds = select([round_table.c.id]).where(
                round_table.c.game_id == g[0]).execute().fetchall()
            games_list[g[0]] = {"players":[]}
            for r in rounds:
                p_ids = select([player_table.c.id]).where(
                    player_table.c.round_id == r[0]).execute().fetchall()
                players = [player[0] for player in p_ids]
                for p in players:
                    games_list[g[0]]["players"].append(p)

        return games_list

    def create_games(self, games_arr):
        self.clear_database()
        game_table = self.meta.tables['game']
        round_table = self.meta.tables['round']
        player_table = self.meta.tables['player']
        for game in games_arr:
            game_table.insert().values().execute()

        i = 0
        for game in game_table.select().execute().fetchall():
            round_table.insert().values(game_id = game[0]).execute()
            round = round_table.select().order_by(
                round_table.c.id.desc()).execute().fetchall()[0]
            for player in range(0,games_arr[i]):
                player_table.insert().values(
                    round_id=round[0],password=uuid.uuid4()).execute()
            i+=1

    def clear_database(self):
        login_table = self.meta.tables['login']
        game_table = self.meta.tables['game']
        move_table = self.meta.tables['move']
        player_table = self.meta.tables['player']
        chat_table = self.meta.tables['chat']
        round_table = self.meta.tables['round']
        rule_table = self.meta.tables['rule']
        vote_table = self.meta.tables['vote']
        login_table.delete().where(player_table.c.id!=-1).execute()
        game_table.delete().where(game_table.c.id!=-1).execute()
        move_table.delete().where(player_table.c.id!=-1).execute()
        player_table.delete().where(player_table.c.id!=-1).execute()
        chat_table.delete().where(player_table.c.id!=-1).execute()
        round_table.delete().where(player_table.c.id!=-1).execute()
        rule_table.delete().where(player_table.c.id!=-1).execute()
        vote_table.delete().where(player_table.c.id!=-1).execute()

        # game_number = 1
        # for player_count in games_arr:
        #     game_table = self.meta.tables['game']
        #     self.con.execute(game_table.insert().values(resource=100))
        #     round_table = self.meta.tables['round']
        #     self.con.execute(round_table.insert().values(game_id = game_number,commons_index = 2000))
        #     for player in range(0,player_count):
        #         player_table = self.meta.tables['player']
        #         self.con.execute(player_table.insert().values(round_id = game_number, name="bob",password="123",worth=0))
            
        #     game_number = game_number+1

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