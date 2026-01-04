import pygame as pg

from engine.scripts.colors import white

class UIFrameBuilder:
    @staticmethod
    def get_ui_frame(width:int, height:int, main_engine_sprite_dict:dict, side_left=True, side_top=True, side_right=True, side_bottom=True) -> pg.Surface:
        surf = pg.Surface((width, height)) # dont forget to ca

        if not UIFrameBuilder.check_for_min_size(width, height, main_engine_sprite_dict):
            print(f"{UIFrameBuilder.__name__}: specified size ({width}, {height}) is too small to be rendered right; returning white square have fun")
            surf.fill(white)

            return surf
        
        ## draw onto the surf
        # load sprites for easier access aka there goes my ram xd
        corners = [
            main_engine_sprite_dict["ui_builder_corner_top_left"],
            main_engine_sprite_dict["ui_builder_corner_top_right"],
            main_engine_sprite_dict["ui_builder_corner_bottom_right"],
            main_engine_sprite_dict["ui_builder_corner_bottom_left"],
        ]

        edges = [
            main_engine_sprite_dict["ui_builder_left"],
            main_engine_sprite_dict["ui_builder_top"],
            main_engine_sprite_dict["ui_builder_right"],
            main_engine_sprite_dict["ui_builder_bottom"],
        ]

        background = main_engine_sprite_dict["ui_builder_background"]

        # rescale
        edges[0] = pg.transform.scale(edges[0], (edges[0].width, height-corners[0].height-corners[3].height))
        edges[1] = pg.transform.scale(edges[1], (width-corners[0].width-corners[1].width, edges[1].height))
        edges[2] = pg.transform.scale(edges[2], (edges[2].width, height-corners[1].height-corners[2].height))
        edges[3] = pg.transform.scale(edges[3], (width-corners[2].width-corners[3].width, edges[3].height))

        background = pg.transform.scale(background, (width-corners[0].width-corners[1].width, height-corners[0].height-corners[3].height))

        # draw
        surf = surf.convert_alpha() #idk if this is right

        surf.blit(corners[0], (0, 0))
        surf.blit(corners[1], (width-corners[1].width, 0))
        surf.blit(corners[2], (width-corners[2].width, height-corners[2].height))
        surf.blit(corners[3], (0, height-corners[3].height))

        surf.blit(edges[0], (0, corners[1].height))
        surf.blit(edges[1], (corners[0].width, 0))
        surf.blit(edges[2], (width-corners[1].width, corners[1].height))
        surf.blit(edges[3], (corners[3].width, height-corners[2].height))

        surf.blit(background, (corners[0].width, corners[0].height))

        return surf

    @staticmethod
    def check_for_min_size(width:int, height:int, sprites:dict) -> bool: # a bit shis, but should be enough to kick me if i do it wrong XD
        if sprites["ui_builder_corner_top_left"].width + sprites["ui_builder_corner_top_right"].width > width:
            return False
        
        if sprites["ui_builder_corner_top_left"].height + sprites["ui_builder_corner_bottom_left"].height > height:
            return False
        
        return True

