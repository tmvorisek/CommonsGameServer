import json
import argparse
import datetime
import smtplib
import getpass
from WebHandlers.database import DBManager
from tornado import websocket
# from GameLogic.ConfigReader import ConfigReader
# from GameLogic.Game import Game
# from GameLogic.GameRules.GameRules import GameRules
# from GameLogic.PlayerActions import PlayerActions
from GameLogicII.game import Game
from GameLogicII.logic_exception import LogicException

from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler

# Start the scheduler
sched = BackgroundScheduler()
sched.start()


# we gonna store clients in dictionary..
clients = dict()

# Gon parse arguments too, y'all.
parser = argparse.ArgumentParser(description='Commons game public python server.')
parser.add_argument('--players', metavar='N', type=int, nargs=1,
                    help='Number of players expected')

db = DBManager()
games_list = {}

def broadcast(obj, game_id):
    message = json.dumps(obj, default=str)
    for c in clients:
        if clients[c]["object"].details["game_id"] == game_id:
            clients[c]["object"].write_message(message)

def compute_game_players_counts(player_count):
    rem = player_count % 8
    groups = int(player_count / 8)
    games = []
    for i in range(0,groups):
        games.append(8)
    if (rem < 4):
        i = 0
        while rem > 0:
            games[i] += 1
            rem -= 1
            i += 1
            if i >= len(games):
                i = 0
    elif (rem >= 4):
        games.append(rem)

    print("Created Games with players counts: " + str(games))
    db.create_games(games)
    return games

def send_admin_email(link_list, admin_email_addr):
    cfg = ConfigReader()
    cfgArgs = cfg.get_rules_from_config('config.json')
    admin_email_addr = cfgArgs['admin_email']
    site_URL = cfgArgs['site_URL']

    if admin_email_addr != '': 
        pass_list = db.get_pass_list()
        link_list = []
        for i in pass_list:
            link_list.append(str("http://" + site_URL + "/user/" + i.encode('ascii', 'ignore')))
    else: 
        return 

    formatted_str_link_list = ''
    for i in link_list:
        formatted_str_link_list += i + '\n'
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    admin_email_pass = getpass.getpass("enter password for " + admin_email_addr + ": ")
    s.login(admin_email_addr, admin_email_pass)
    msg = 'Subject: {}\n\n{}'.format('Commons game Link List', formatted_str_link_list)
    s.sendmail(admin_email_addr, admin_email_addr, msg)

def reload_games():
    moves = db.load_games()
    # action_lookup = {"sustain":0,"police":3,"overharvest":1,"invest":2}
    for game_id in moves:
        game = Game(len(moves[game_id]["players"]), game_id)
        games_list[game_id] = game
        active_summit = 0
        for move in moves[game_id]["moves"]:
            if move["summit_index"] > active_summit:
                game.finish_summit()
            try:
                game.add_move(move["player_index"], move["harvest"])
            except:
                pass

    return games_list

def finish_summit():
    print("Running nightly routines...")
    i = 0
    for game_id in games_list:
        game = games_list[game_id]
        if not game.is_last_summit():
            i = 1
            game.finish_summit()
            db.new_summit(game.game_id, game.get_commons_index())
    if i > 0:
        periodic_update()
    print("Nightly update complete")

def periodic_update():
    # exec_date = datetime.date.today() + datetime.timedelta(minutes=1)
    sched.add_job(finish_summit, "interval", days=1)

periodic_update()

class WebSocketHandler(websocket.WebSocketHandler):
    action_lookup = {"sustain":0,"police":3,"overharvest":1,"invest":2}
    args = parser.parse_args()
    if args.players:
        compute_game_players_counts(args.players[0])
        exit()

    games_list = reload_games()

    # send_admin_email(link_list, admin_email_addr)

    def on_message(self, message):        
        msg = json.loads(message);
        print(msg)
        if 'type' not in msg:
            return
        elif msg['type'] == 'chat':
            if len(msg['text']) == 0:
                return
            self.chat(msg)
        elif msg['type'] == 'name':
            if len(msg['name']) != 0:
                db.set_name(self.id, msg['name'])
                self.details['name'] = msg['name']
        elif msg['type'] == 'game_data':
            self.handleData(msg)
        elif msg['type'] == 'move':
            self.move(msg)

    def on_close(self):
        if hasattr(self, 'id'):
            del clients[self.id]

    def open(self):
        self.stream.set_nodelay(True)
        cookie = self.get_secure_cookie("commons_pass")
        if(cookie):
            self.id = db.check_pass(cookie.decode())
            clients[self.id] = {"id": self.id, "object": self}

            self.details = db.get_player_details(self.id)
            self.game = self.games_list[self.details["game_id"]]
            self.player_index = self.details["player_index"]
            self.player = self.game.get_player(self.player_index)
            self.details["active_round"] = self.player.active_round
            self.details["commons_index"] = float(self.game.get_commons_index())
            self.details["max_round"] = self.game.config["rounds_per_summit"]
            self.details["wealth"] = self.player.wealth
            self.send(self.details)

            chat_log = db.get_chats(self.details["game_id"])
            for round_chats in chat_log:
                for chat in round_chats:
                    obj = {
                        "type":"chat",
                        "text":chat[2],
                        "name":chat[7],
                        "time":chat[3],
                        "round_id":chat[4],
                        "player_id":chat[5],
                    }
                    self.send(obj)

            obj = {"type": "scoreboard",
                    "scoreboard":self.game.get_scoreboard_for_player(self.player_index)}
            self.send(obj)


    def move(self, msg):
        if msg["move"] in ["sustain","police","overharvest","invest"]:
            try:
                self.game.add_move(self.player_index, msg["move"])
            except LogicException as e:
                self.send_error(e)
                finish_summit()
                summit_id = db.get_summit_id(
                    self.game.active_summit_index,
                    self.details["game_id"])
                db.store_move(self.id, 
                    summit_id,
                    msg["move"])
            else:
                summit_id = db.get_summit_id(
                    self.game.active_summit_index,
                    self.details["game_id"])
                db.store_move(self.id, 
                    summit_id,
                    msg["move"])
                msg["round_index"] = self.player.active_round
                msg["player_id"] = self.id
                self.send(msg)

            # score_board = self.game.get_player_score_board(self.player_index)
            # print score_board



    def chat(self,msg):
        msg['player_id'] = self.id;
        msg['summit_id'] = self.details['summit_id']
        msg['name'] = self.details['name']
        msg['time'] = datetime.datetime.now()
        msg['text'].replace('<','').replace('>','')
        db.store_chat(msg)
        broadcast(msg, self.details['game_id'])

    def send(self, obj):
        message = json.dumps(obj, default=str)
        self.write_message(message)

    def send_error(self, error):
        message = json.dumps({ "type": "error",
                    "message": str(error)}, default=str)
        self.write_message(message)

