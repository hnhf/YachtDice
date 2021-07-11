class Room:
    def __init__(self, num):
        self.num = num
        self.players = []
        self.seats = 2
        self.player_location = []

    def add_player(self, player):
        player_num = len(self.players)
        if player_num > 1:
            return False
        self.players.append(player.name)
        self.player_location.append({"player": player.name, "location": player_num})
        return True
