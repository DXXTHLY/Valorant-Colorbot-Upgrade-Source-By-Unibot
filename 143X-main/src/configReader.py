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

from configparser import ConfigParser
import numpy as np
import os


class ConfigReader:
    def __init__(self):
        self.parser = ConfigParser()

        # Communication
        self.com_type = None
        self.ip = None
        self.port = None
        self.com_port = None

        # Screen
        self.detection_threshold = None
        self.upper_color = None
        self.lower_color = None
        self.fov_x = None
        self.fov_y = None
        self.aim_fov_x = None
        self.aim_fov_y = None
        self.fps = None
        self.auto_detect_resolution = None
        self.resolution_x = None
        self.resolution_y = None

        # Aim
        self.offset = None
        self.smooth = None
        self.speed = None
        self.y_speed = None
        self.aim_height = None

        # Recoil
        self.recoil_mode = None
        self.recoil_x = None
        self.recoil_y = None
        self.max_offset = None
        self.recoil_recover = None

        # Trigger
        self.trigger_delay = None
        self.trigger_randomization = None
        self.trigger_threshold = None

        # Rapid fire
        self.target_cps = None

        # Key binds
        self.key_reload_config = None
        self.key_toggle_aim = None
        self.key_toggle_recoil = None
        self.key_exit = None
        self.key_trigger = None
        self.key_rapid_fire = None
        self.aim_keys = []

        # Debug
        self.debug = None
        self.debug_always_on = None
        self.display_mode = None

        # Get config path and read it
        self.path = os.path.join(os.path.dirname(__file__), '../config.ini')
        self.parser.read(self.path)

    def read_config(self):
        # Get communication settings
        self.com_type = self.get_config_value('communication', 'type', 'none', ['none', 'driver', 'serial', 'socket'])
        
        if self.com_type == 'socket':
            self.ip = self.parser.get('communication', 'ip')
            self.port = self.parser.getint('communication', 'port')
        elif self.com_type == 'serial':
            self.com_port = self.parser.get('communication', 'com_port')

        # Get screen settings
        self.detection_threshold = self.parse_tuple('screen', 'detection_threshold')
        self.upper_color = self.parse_color('screen', 'upper_color')
        self.lower_color = self.parse_color('screen', 'lower_color')

        self.fov_x = self.parser.getint('screen', 'fov_x')
        self.fov_y = self.parser.getint('screen', 'fov_y')
        self.aim_fov_x = self.parser.getint('screen', 'aim_fov_x')
        self.aim_fov_y = self.parser.getint('screen', 'aim_fov_y')
        fps_value = self.parser.getint('screen', 'fps')
        self.fps = int(np.floor(1000 / fps_value + 1))

        self.auto_detect_resolution = self.parse_bool('screen', 'auto_detect_resolution')
        self.resolution_x = self.parser.getint('screen', 'resolution_x')
        self.resolution_y = self.parser.getint('screen', 'resolution_y')

        # Get aim settings
        self.offset = self.parser.getint('aim', 'offset')
        self.smooth = self.parse_smooth('aim', 'smooth')
        self.speed = self.parser.getfloat('aim', 'speed')
        self.y_speed = self.parser.getfloat('aim', 'y_speed')
        self.aim_height = self.parse_float_range('aim', 'aim_height', 0, 1)

        # Get recoil settings
        self.recoil_mode = self.get_config_value('recoil', 'mode', 'move', ['move', 'offset'])
        self.recoil_x = self.parser.getfloat('recoil', 'recoil_x')
        self.recoil_y = self.parser.getfloat('recoil', 'recoil_y')
        self.max_offset = self.parser.getint('recoil', 'max_offset')
        self.recoil_recover = self.parser.getfloat('recoil', 'recover')

        # Get trigger settings
        self.trigger_delay = self.parser.getint('trigger', 'trigger_delay')
        self.trigger_randomization = self.parser.getint('trigger', 'trigger_randomization')
        self.trigger_threshold = self.parser.getint('trigger', 'trigger_threshold')

        # Get rapid fire settings
        self.target_cps = self.parser.getint('rapid_fire', 'target_cps')

        # Get keybind settings
        self.key_reload_config = self.read_hex(self.parser.get('key_binds', 'key_reload_config'))
        self.key_toggle_aim = self.read_hex(self.parser.get('key_binds', 'key_toggle_aim'))
        self.key_toggle_recoil = self.read_hex(self.parser.get('key_binds', 'key_toggle_recoil'))
        self.key_exit = self.read_hex(self.parser.get('key_binds', 'key_exit'))
        self.key_trigger = self.read_hex(self.parser.get('key_binds', 'key_trigger'))
        self.key_rapid_fire = self.read_hex(self.parser.get('key_binds', 'key_rapid_fire'))
        self.aim_keys = self.read_aim_keys(self.parser.get('key_binds', 'aim_keys'))

        # Get debug settings
        self.debug = self.parse_bool('debug', 'enabled')
        self.debug_always_on = self.parse_bool('debug', 'always_on')
        self.display_mode = self.get_config_value('debug', 'display_mode', 'game', ['game', 'mask'])

    def get_config_value(self, section, option, default, valid_values):
        value = self.parser.get(section, option).lower()
        if value in valid_values:
            return value
        else:
            print(f'WARNING: Invalid {option} value in section {section}, using default ({default})')
            return default

    def parse_tuple(self, section, option):
        values_str = self.parser.get(section, option).split(',')
        return tuple(int(x.strip()) for x in values_str)

    def parse_color(self, section, option):
        color = self.parser.get(section, option).split(',')
        return np.array([int(x.strip()) for x in color])

    def parse_bool(self, section, option):
        return self.parser.get(section, option).lower() == 'true'

    def parse_smooth(self, section, option):
        value = float(self.parser.get(section, option))
        if 0 <= value <= 1:
            return 1 - value / 1.25
        else:
            print(f'WARNING: Invalid {option} value')
            return None

    def parse_float_range(self, section, option, min_value, max_value):
        value = float(self.parser.get(section, option))
        if min_value <= value <= max_value:
            return value
        else:
            print(f'WARNING: Invalid {option} value')
            return None

    def read_hex(self, string):
        return int(string, 16)

    def read_aim_keys(self, keys_str):
        if keys_str == 'off':
            return ['off']
        return [self.read_hex(key) for key in keys_str.split(',')]
