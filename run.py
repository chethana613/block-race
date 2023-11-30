import game
from network import Network

if __name__ == "__main__":
    g = game.Game(500,500)

    net = Network()
    if(net.connected):
        g.run()