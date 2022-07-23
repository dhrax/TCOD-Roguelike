#!/usr/bin/env python3
import copy
from numpy import isin
import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler
import entity_factories
from engine import Engine
from procgen import generate_dungeon


def main() -> None:

    print("Hiya")

    screen_width = 80
    screen_height = 50

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2

    player = copy.deepcopy(entity_factories.player)
    
    game_map = generate_dungeon(max_rooms=max_rooms, room_max_size=room_max_size,
    room_min_size=room_min_size, map_width=80, map_height=50, player=player,
    max_monsters_per_room= max_monsters_per_room)

    event_handler = EventHandler()

    engine = Engine(event_handler=event_handler, player=player, game_map=game_map)

    tileset = tcod.tileset.load_tilesheet(".\\resources\\tileset.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    

    with tcod.context.new_terminal(
        game_map.width,
        game_map.height,
        tileset=tileset,
        title = "New Roguelike",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:

            engine.render(root_console, context)

            events = tcod.event.wait()
            engine.handle_events(events)


    

if __name__ == "__main__":
    main()  