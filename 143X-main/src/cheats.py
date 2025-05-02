# Consider donating: https://github.com/vike256#donate
# Please follow: https://github.com/dxxthly
#
# Unibot (Upgraded by DXXTHLY, originally created by vike256) is an open-source colorbot.
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


class Cheats:
    def __init__(self, config):
        """
        Initialize the cheats object with configuration parameters.

        Args:
        config (Config): Configuration object containing settings for recoil, aim speed, etc.
        """
        # Aim settings
        self.move_x, self.move_y = 0, 0
        self.previous_x, self.previous_y = 0, 0
        self.smooth = config.smooth
        self.speed = config.speed
        self.y_speed = config.y_speed

        # Recoil settings
        self.recoil_offset = 0
        self.recoil_mode = config.recoil_mode
        self.recoil_x = config.recoil_x
        self.recoil_y = config.recoil_y
        self.max_offset = config.max_offset
        self.recoil_recover = config.recoil_recover

    def calculate_aim(self, state, target):
        """
        Calculate the aiming adjustments based on the target and apply smoothing.

        Args:
        state (bool): Whether the aim feature is enabled.
        target (tuple): The target position (x, y).
        """
        if state and target is not None:
            x, y = target

            # Apply speed multipliers
            x *= self.speed
            y *= self.speed * self.y_speed

            # Apply smoothing
            x = (1 - self.smooth) * self.previous_x + self.smooth * x
            y = (1 - self.smooth) * self.previous_y + self.smooth * y

            # Store current values for next frame
            self.previous_x, self.previous_y = x, y

            # Update movement variables
            self.move_x, self.move_y = x, y

    def apply_recoil(self, state, delta_time):
        """
        Apply recoil effect based on the current mode and mouse button state.

        Args:
        state (bool): Whether the recoil feature is enabled.
        delta_time (float): The time passed since the last frame.
        """
        if not state or delta_time == 0:
            # Reset recoil offset if recoil is off or no time has passed
            self.recoil_offset = 0
            return

        # Cache mouse button state (left click)
        mouse_button_down = win32api.GetAsyncKeyState(0x01) < 0

        if self.recoil_mode == 'move' and mouse_button_down:
            # Apply recoil to movement directly
            self.move_x += self.recoil_x * delta_time
            self.move_y += self.recoil_y * delta_time

        elif self.recoil_mode == 'offset':
            if mouse_button_down:
                # Increase recoil offset but don't exceed the max limit
                self.recoil_offset = min(self.recoil_offset + self.recoil_y * delta_time, self.max_offset)
            else:
                # Gradually decrease recoil offset when mouse button is released
                self.recoil_offset = max(self.recoil_offset - self.recoil_recover * delta_time, 0)
