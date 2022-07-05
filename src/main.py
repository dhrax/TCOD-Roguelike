#!/usr/bin/env python3
from html import entities
from numpy import isin
import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler
from entity import Entity
from engine import Engine
from game_map import GameMap


def main() -> None:

    print("Hiya")

    screen_width = 80
    screen_height = 50

    game_map = GameMap(width=80, height=50)

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", [255, 255, 255])
    npc = Entity(int(screen_width / 2 - 10), int(screen_height / 2 - 10), "N", [255, 255, 0])

    entities = {player, npc}

    event_handler = EventHandler()

    engine = Engine(entities=entities, event_handler=event_handler, player=player, game_map=game_map)

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