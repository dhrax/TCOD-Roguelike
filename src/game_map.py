import numpy as np  # type: ignore
from tcod.console import Console

import tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        #fill the map with a specified tile type
        #self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        #self.tiles[30:33, 22] = tile_types.wall

        self.visible_tiles = np.full((width, height), fill_value=False, order="F")
        self.explored_tiles = np.full((width, height), fill_value=False, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible_tiles, self.explored_tiles],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )