from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from input_handlers import EventHandler
from game_map import GameMap


class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, player: Entity, game_map: GameMap):
        self.entities = entities
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map

        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            
            action.perform(self, self.player)

            self.update_fov()

    def render(self, console: Console, context: Context) -> None:

        self.game_map.render(console)

        for entity in self.entities:
            # Only print entities that are in the FOV
            if self.game_map.visible_tiles[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        #updates the screen
        context.present(console)

        console.clear()

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible_tiles[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored_tiles |= self.game_map.visible_tiles
