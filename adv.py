from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


# Reverse direction when no other path is available
def get_reverse_direction(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'


# Create a traversal path to explore all rooms
def generate_traversal_path(graph):

    # List for generated path
    generated_path = []

    # List for backtracking
    backtrack = []

    # Keep track of visited rooms
    visited = {}

    # Keep track of unexplored rooms
    unexplored = {}

    # Loops through while there are unexplored rooms
    while len(visited) < len(room_graph):

        # Initial starting point for visited and unexplored
        if len(visited) == 0:
            current_room = player.current_room.id
            current_exits = player.current_room.get_exits()
            visited[current_room] = current_exits
            unexplored[current_room] = current_exits

        # Check if current room was visited
        if player.current_room.id not in visited:
            # If not, add current room to visited and unexplored
            visited[player.current_room.id] = player.current_room.get_exits()
            unexplored[player.current_room.id] = player.current_room.get_exits()

        # If there's no more directions for current room, then backtrack
        while len(unexplored[player.current_room.id]) < 1:
            reverse_direction = backtrack.pop()
            generated_path.append(reverse_direction)
            player.travel(reverse_direction)

        # Get direction to move in
        move = unexplored[player.current_room.id].pop()

        # Add direction to generated path
        generated_path.append(move)

        # Add reverse direction to backtrack list
        backtrack.append(get_reverse_direction(move))

        # Move player to the room to update current room
        player.travel(move)

    # return list of directions
    return generated_path

# Update traversal path list
traversal_path.extend(generate_traversal_path(room_graph))


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
