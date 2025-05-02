# Consider donating: https://github.com/vike256#donate
# Please follow: https://github.com/dxxthly
#
# 143X (Upgraded by DXXTHLY, originally created by vike256) is an open-source colorbot.
# Copyright (C) 2025 DXXTHLY (modified version)
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.

import time
import numpy as np
import logging

from cheats import Cheats
from mouse import Mouse
from screen import Screen
from utils import Utils

def initialize_components():
    """Initialize all components outside the main loop to avoid re-initialization."""
    utils = Utils()
    config = utils.config
    cheats = Cheats(config)
    mouse = Mouse(config)
    screen = Screen(config)
    return utils, config, cheats, mouse, screen

def process_target(utils, screen, cheats, mouse):
    """Process the target, apply aim and trigger actions."""
    target, trigger = screen.get_target(cheats.recoil_offset)
    
    if utils.get_trigger_state() and trigger:
        if utils.config.trigger_delay != 0:
            delay_before_click = (np.random.randint(utils.config.trigger_randomization) + utils.config.trigger_delay) / 1000
        else:
            delay_before_click = 0
        mouse.click(delay_before_click)

    cheats.calculate_aim(utils.get_aim_state(), target)

def process_rapid_fire(utils, mouse):
    """Handle rapid fire actions."""
    if utils.get_rapid_fire_state():
        mouse.click()

def process_recoil(cheats, utils, delta_time):
    """Apply recoil and reset aim drift."""
    cheats.apply_recoil(utils.recoil_state, delta_time)
    cheats.move_x, cheats.move_y = (0, 0)  # Reset move to prevent drift when no target

def main():
    # Set up logging for better debugging and tracking
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    # Print licensing info
    print('''143X  Copyright (C) 2025 DXXTHLY
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.
For details see <LICENSE.txt>.
    ''')

    # Print donation info
    print('Consider donating: https://github.com/vike256#donate \n')

    # Mention the person modifying the code
    print('This version has been modified by DXXTHLY. Check out the GitHub: https://github.com/dxxthly \n')

    # Initialize components once before starting the main loop
    utils, config, cheats, mouse, screen = initialize_components()

    logging.info('143X ON')

    # Program loop
    while True:
        # Track delta time
        start_time = time.time()

        # Cheat loop
        while True:
            delta_time = time.time() - start_time
            start_time = time.time()
            
            reload_config = utils.check_key_binds()
            if reload_config:
                logging.info('Reloading configuration...')
                break

            if (utils.get_aim_state() or utils.get_trigger_state()) or (config.debug and config.debug_always_on):
                # Process target and aim
                process_target(utils, screen, cheats, mouse)

            # Handle rapid fire
            process_rapid_fire(utils, mouse)

            # Apply recoil and reset movements
            process_recoil(cheats, utils, delta_time)

            # Move mouse based on calculated aim
            mouse.move(cheats.move_x, cheats.move_y)

            # Ensure frame rate consistency by adjusting the sleep time
            time_spent = (time.time() - start_time) * 1000
            if time_spent < screen.fps:
                time.sleep((screen.fps - time_spent) / 1000)

        # Cleanup and prepare for reloading the configuration
        del utils
        del cheats
        del mouse
        del screen
        logging.info('143X reloading...')

if __name__ == "__main__":
    main()
