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
import win32api
import win32con
import serial
import socket
import threading
import logging
from concurrent.futures import ThreadPoolExecutor


class Mouse:
    def __init__(self, config):
        self.com_type = config.com_type
        self.last_click_time = time.time()
        self.target_cps = config.target_cps
        self.lock = threading.Lock()

        # Connection setup based on communication type
        self.setup_connection(config)

        # Remainder variables for smooth mouse movement
        self.remainder_x = 0
        self.remainder_y = 0

        # ThreadPoolExecutor to manage threads better
        self.executor = ThreadPoolExecutor(max_workers=2)

    def setup_connection(self, config):
        """Set up communication connection based on the config type."""
        self.ip = config.ip
        self.port = config.port
        self.client = None
        self.board = None

        try:
            if self.com_type == 'socket':
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect((self.ip, self.port))
                logging.info(f"Connected to socket {self.ip}:{self.port}")
            elif self.com_type == 'serial':
                self.board = serial.Serial(config.com_port, 115200)
                logging.info("Connected to serial port.")
            elif self.com_type == 'driver':
                import interception
                interception.auto_capture_devices(mouse=True)
                logging.info("Driver connection initialized.")
        except Exception as e:
            logging.error(f"Error during connection setup: {e}")
            self.close_connection()

    def __del__(self):
        self.close_connection()

    def close_connection(self):
        """Close the communication connection safely."""
        if self.com_type == 'socket' and self.client:
            self.client.close()
            logging.info("Socket connection closed.")
        elif self.com_type == 'serial' and self.board:
            self.board.close()
            logging.info("Serial connection closed.")

    def move(self, x, y):
        """Move the mouse, including handling remainder values for precision."""
        x += self.remainder_x
        y += self.remainder_y

        # Round the values and update remainders
        self.remainder_x, self.remainder_y = x - int(x), y - int(y)
        x, y = int(x), int(y)

        if x != 0 or y != 0:
            self.executor.submit(self._send_move, x, y)

    def _send_move(self, x, y):
        """Send the move command based on the connection type."""
        match self.com_type:
            case 'socket' | 'serial':
                self.send_command(f'M{x},{y}\r')
            case 'driver':
                import interception
                interception.move_relative(x, y)
                logging.debug(f"Moved mouse by {x}, {y}")
            case 'none':
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
                logging.debug(f"Moved mouse by {x}, {y}")

    def click(self, delay_before_click=0):
        """Initiate a click with optional delay."""
        if time.time() - self.last_click_time >= 1 / self.target_cps:
            self.executor.submit(self._send_click, delay_before_click)

    def _send_click(self, delay_before_click=0):
        """Send the click command after a delay."""
        time.sleep(delay_before_click)
        self.last_click_time = time.time()

        match self.com_type:
            case 'socket' | 'serial':
                self.send_command('C\r')
            case 'driver':
                self._driver_click()
            case 'none':
                self._mouse_event_click()

    def _driver_click(self):
        """Handle click for the 'driver' communication type."""
        import interception
        random_delay = np.random.randint(40, 80) / 1000
        interception.mouse_down('left')
        time.sleep(random_delay)
        interception.mouse_up('left')
        logging.debug(f"Click performed with delay: {random_delay * 1000:g}ms")

    def _mouse_event_click(self):
        """Handle click for 'none' communication type using win32api."""
        random_delay = np.random.randint(40, 80) / 1000
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(random_delay)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        logging.debug(f"Click performed with delay: {random_delay * 1000:g}ms")

        # Prevent double clicks too quickly
        time.sleep(np.random.randint(25, 35) / 1000)

    def send_command(self, command):
        """Send a command to the connected device or server."""
        with self.lock:
            match self.com_type:
                case 'socket':
                    self.client.sendall(command.encode())
                case 'serial':
                    self.board.write(command.encode())
            logging.debug(f"Sent command: {command}")
            response = self.get_response()
            logging.debug(f"Response: {response}")

    def get_response(self):
        """Get a response from the communication device."""
        match self.com_type:
            case 'socket':
                return self.client.recv(4).decode()
            case 'serial':
                while True:
                    receive = self.board.readline().decode('utf-8').strip()
                    if len(receive) > 0:
                        return receive
