# Block Race online multi-player game

An online multiplayer game where multiple users race their blocks towards the goal. An in-game chat feature is implemented for players to create/join groups and communicate with other players in the game network. The game and chat feature are implemented using TCP and socket programming in Python.

# Game Features:

1. Multiple clients can connect to the server, and the server can handle requests from multiple clients.
2. Color Codes:
    - Blue Block: Initial state of the opponent player.
    - Red Block: Current player's move.
    - Yellow Block: Opponent player's move.
    - Green Block: Winner.
    - Black Block: Loser.
    - Note: When a new player joins the network as an opponent, their block color changes from blue to yellow on the initial player's screen.
4. Players can move their blocks on their canvas.
5. Winner: The first player to reach the goal with their block wins.
6. Chat: 
    - Players can create a new room or join existing chat rooms
    - Players can send messages in the chat room
    - Players can leave/quit the chat room
    - Players can list the users in the chat room

# Other Features:

1. Clients can gracefully handle server crashes and exceptions
2. Server can gracefully handle unresponsive/crashed clients
