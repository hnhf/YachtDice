class Room:
    def __init__(self, num):
        self.num = num
        self.players = []
        self.seats = 2
        self.player_location = []
        self.is_gaming = False

    def add_player(self, player):
        player_num = len(self.players)
        if player_num > 1:
            return False
        self.players.append(player)
        self.player_location.append({"player": player.name, "location": player_num})
        return self.player_location

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)
        else:
            return
