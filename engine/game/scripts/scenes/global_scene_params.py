from scripts.core.settings import WIDTH, HEIGHT

class GlobalSceneParams:

    # TITLE
    title_button_width = 280
    title_button_height = 128
    title_square_button_size = 128
    title_side_button_x_distance = 250
    title_button_y_offset = 160 # not sure why this cant be the same as button x dist ::


    # MAIN MENU
    main_menu_button_start_y = 750 # all values autoconverted by to_scale_x/y
    main_menu_button_width = title_button_width
    main_menu_button_height = title_button_height
    main_menu_button_y_offset = title_button_y_offset

    main_menu_background_frame_width = 1600
    main_menu_background_frame_height = 600
    main_menu_background_frame_x = (WIDTH - main_menu_background_frame_width) / 2
    main_menu_background_frame_y = 100

    main_menu_background_frame_width_part = main_menu_background_frame_width / 10
    main_menu_background_frame_margin = 20

    main_menu_ship_frame_width = main_menu_background_frame_width_part * 5 - 2 * main_menu_background_frame_margin
    main_menu_mode_frame_width = main_menu_background_frame_width_part * 3 - 2 * main_menu_background_frame_margin
    main_menu_news_frame_width = main_menu_background_frame_width_part * 2 - 2 * main_menu_background_frame_margin

    main_menu_ship_frame_x = main_menu_background_frame_x + main_menu_background_frame_margin
    main_menu_mode_frame_x = main_menu_ship_frame_x + main_menu_ship_frame_width + 2 * main_menu_background_frame_margin
    main_menu_news_frame_x = main_menu_mode_frame_x + main_menu_mode_frame_width + 2 * main_menu_background_frame_margin
    
    ship_window_size_mult = 0.4
    ship_window_size = (main_menu_ship_frame_width * ship_window_size_mult, main_menu_ship_frame_width * ship_window_size_mult)
    ship_window_pos = (main_menu_ship_frame_x + (main_menu_ship_frame_width - ship_window_size[0]) / 2, main_menu_background_frame_y + (main_menu_background_frame_height - ship_window_size[1]) / 2 - 50) # ja uz asi nedavam matiku pls proc 4 a ne 2

    mode_button_size = (360, 146)
    mode_button_margin = 40
    mode_button_start_pos = (main_menu_mode_frame_x + mode_button_margin, main_menu_background_frame_y + mode_button_margin)

    ship_switch_size = (128, 280)
    ship_switch_left_button_pos = (main_menu_ship_frame_x + 30, main_menu_background_frame_y + (main_menu_background_frame_height - ship_switch_size[1]) / 2)
    ship_switch_right_button_pos = (main_menu_ship_frame_x - 30 + main_menu_ship_frame_width - ship_switch_size[0], main_menu_background_frame_y + (main_menu_background_frame_height - ship_switch_size[1]) / 2)

    ship_mod_button_size = (main_menu_button_width, main_menu_button_height)
    ship_mod_button_pos = (main_menu_ship_frame_x + (main_menu_ship_frame_width - ship_mod_button_size[0]) / 2, main_menu_background_frame_y + 420)


    # SHIP MODIFICATION
    ship_mod_background_frame_size = (1600, 900)
    ship_mod_background_frame_pos = (
        (WIDTH - ship_mod_background_frame_size[0]) / 2,
        (HEIGHT - ship_mod_background_frame_size[1]) / 2
    )

    ship_mod_return_button_margin = 25
    ship_mod_return_button_size = 128

    ship_mod_slot_button_size = 100


    # CAREER
    career_background_frame_size = (1600, 900)
    career_background_frame_pos = (
        (WIDTH - career_background_frame_size[0]) / 2,
        (HEIGHT - career_background_frame_size[1]) / 2
    )

    career_return_button_margin = 25
    career_return_button_size = 128

    career_selector_element_margin  = 25
    career_selector_element_height  = 128 # also the button size
    career_selector_display_width   = 700

    career_level_decoration_window_size = (300, career_background_frame_size[1] - 300)
    career_level_window_size = (career_background_frame_size[0] - 600, career_level_decoration_window_size[1])
    
    career_level_decoration_window_pos = (
        career_background_frame_pos[0] + 100,
        career_background_frame_pos[1] + (career_background_frame_size[1] - career_level_decoration_window_size[1]) / 2 + 100
    )

    career_level_window_pos = (
        career_level_decoration_window_pos[0] + career_level_decoration_window_size[0] + 20,
        career_level_decoration_window_pos[1]
    )