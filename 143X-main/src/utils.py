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

import win32api
from time import sleep
import logging
from configReader import ConfigReader

# Setting up logging for better traceability and debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')


class Utils:
    def __init__(self):
        self.config = ConfigReader()
        self.reload_config()

        self.delay = 0.25
        self.key_reload_config = self.config.key_reload_config
        self.key_toggle_aim = self.config.key_toggle_aim
        self.key_toggle_recoil = self.config.key_toggle_recoil
        self.key_exit = self.config.key_exit
        self.key_trigger = self.config.key_trigger
        self.key_rapid_fire = self.config.key_rapid_fire
        self.aim_keys = self.config.aim_keys
        self.aim_state = False
        self.recoil_state = False

        self.key_states = {  # Caching the key states
            "reload_config": False,
            "toggle_aim": False,
            "toggle_recoil": False,
            "exit": False,
            "trigger": False,
            "rapid_fire": False
        }

    def check_key_binds(self):
        """Check for key presses and perform actions accordingly."""
        if self._key_pressed(self.key_reload_config):
            logging.info("Reloading config")
            return True  # Signal to reload config

        if self._key_pressed(self.key_toggle_aim):
            self.aim_state = not self.aim_state
            logging.info(f"AIM: {self.aim_state}")
            sleep(self.delay)

        if self._key_pressed(self.key_toggle_recoil):
            self.recoil_state = not self.recoil_state
            logging.info(f"RECOIL: {self.recoil_state}")
            sleep(self.delay)

        if self._key_pressed(self.key_exit):
            logging.info("Exiting")
            exit(1)  # Gracefully exit the program

        return False

    def reload_config(self):
        """Reload configuration from the config reader."""
        try:
            self.config.read_config()
        except Exception as e:
            logging.error(f"Error reloading config: {e}")

    def get_aim_state(self):
        """Returns whether the aim state is active."""
        if self.aim_state:
            if self.aim_keys[0] == 'off':
                return True
            return any(self._key_pressed(key) for key in self.aim_keys)
        return False

    def get_trigger_state(self):
        """Returns whether the trigger state is active."""
        return self._key_pressed(self.key_trigger)

    def get_rapid_fire_state(self):
        """Returns whether the rapid fire state is active."""
        return self._key_pressed(self.key_rapid_fire)

    def _key_pressed(self, key):
        """Helper function to check if a key is pressed, caching the state."""
        if self.key_states.get(key, False):
            return False
        key_state = win32api.GetAsyncKeyState(key) < 0
        self.key_states[key] = key_state
        return key_state

    @staticmethod
    def print_attributes(obj):
        """Prints all the attributes of an object."""
        try:
            attributes = vars(obj)
            for attribute, value in attributes.items():
                print(f'{attribute}: {value}')
        except Exception as e:
            logging.error(f"Error printing attributes: {e}")


# Example of how to use logging and caching:
if __name__ == "__main__":
    utils = Utils()
    while True:
        if utils.check_key_binds():
            utils.reload_config()  # Handle config reload
        sleep(0.1)
