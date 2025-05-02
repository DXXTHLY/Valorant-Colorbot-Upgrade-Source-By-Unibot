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

import cv2
import numpy as np
import bettercam
from pyautogui import size
import logging


class Screen:
    def __init__(self, config):
        self.cam = bettercam.create(output_color="BGR")
        self.offset = config.offset

        self.screen = self._get_screen_resolution(config)
        self.screen_center = (self.screen[0] // 2, self.screen[1] // 2)
        self.screen_region = (0, 0, self.screen[0], self.screen[1])
        self.fov = (config.fov_x, config.fov_y)
        self.fov_center = (self.fov[0] // 2, self.fov[1] // 2)
        self.fov_region = self._calculate_fov_region()
        
        self.detection_threshold = config.detection_threshold
        self.upper_color = config.upper_color
        self.lower_color = config.lower_color
        self.fps = config.fps
        self.aim_height = config.aim_height
        self.debug = config.debug
        self.trigger_threshold = config.trigger_threshold
        self.aim_fov = (config.aim_fov_x, config.aim_fov_y)

        self.thresh = None
        self.target = None
        self.closest_contour = None
        self.img = None

        # Setup debug display if enabled
        if self.debug:
            self.display_mode = config.display_mode
            self.window_name = 'Python'
            self.window_resolution = (self.screen[0] // 2, self.screen[1] // 2)
            cv2.namedWindow(self.window_name)

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

    def __del__(self):
        del self.cam

    def _get_screen_resolution(self, config):
        """Returns screen resolution, either auto-detected or from config."""
        if config.auto_detect_resolution:
            screen_size = size()
            return (screen_size.width, screen_size.height)
        else:
            return (config.resolution_x, config.resolution_y)

    def _calculate_fov_region(self):
        """Calculate the Field of View (FOV) region."""
        return (
            self.screen_center[0] - self.fov[0] // 2,
            self.screen_center[1] - self.fov[1] // 2 - self.offset,
            self.screen_center[0] + self.fov[0] // 2,
            self.screen_center[1] + self.fov[1] // 2 - self.offset
        )

    def screenshot(self, region):
        """Capture a screenshot from the camera."""
        try:
            image = self.cam.grab(region)
            if image is not None:
                return np.array(image)
        except Exception as e:
            logging.error(f"Error capturing screenshot: {e}")
            return None

    def get_target(self, recoil_offset):
        """Identify the closest target based on the specified recoil offset."""
        recoil_offset = int(recoil_offset)
        self.target, trigger = None, False
        self.closest_contour = None

        # Capture screenshot within FOV region
        self.img = self.screenshot(self.get_region(self.fov_region, recoil_offset))
        if self.img is None:
            return None, False

        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_color, self.upper_color)
        kernel = np.ones((self.detection_threshold[0], self.detection_threshold[1]), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=5)

        # Apply thresholding
        self.thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if contours:
            trigger = self._find_closest_target(contours)

        if self.debug:
            self.debug_display(recoil_offset)

        return self.target, trigger

    def _find_closest_target(self, contours):
        """Find the closest target by distance from crosshair."""
        min_distance = float('inf')
        for contour in contours:
            rect_x, rect_y, rect_w, rect_h = cv2.boundingRect(contour)
            x = rect_x + rect_w // 2 - self.fov_center[0]
            y = int(rect_y + rect_h * (1 - self.aim_height)) - self.fov_center[1]
            distance = np.sqrt(x**2 + y**2)

            if distance < min_distance:
                min_distance = distance
                self.closest_contour = contour
                if -self.aim_fov[0] <= x <= self.aim_fov[0] and -self.aim_fov[1] <= y <= self.aim_fov[1]:
                    self.target = (x, y)

        # Check if crosshair is inside the closest target
        if self.closest_contour and self._check_crosshair_in_target():
            return True
        return False

    def _check_crosshair_in_target(self):
        """Check if the crosshair is within the closest target."""
        checks = [
            (self.fov_center[0], self.fov_center[1]),
            (self.fov_center[0] + self.trigger_threshold, self.fov_center[1]),
            (self.fov_center[0] - self.trigger_threshold, self.fov_center[1]),
            (self.fov_center[0], self.fov_center[1] + self.trigger_threshold),
            (self.fov_center[0], self.fov_center[1] - self.trigger_threshold)
        ]
        return all(
            cv2.pointPolygonTest(self.closest_contour, point, False) >= 0
            for point in checks
        )

    @staticmethod
    def get_region(region, recoil_offset):
        """Return the region adjusted for recoil offset."""
        return (
            region[0],
            region[1] - recoil_offset,
            region[2],
            region[3] - recoil_offset
        )

    def debug_display(self, recoil_offset):
        """Display debug information on the captured image."""
        debug_img = self.img if self.display_mode == 'game' else self._prepare_debug_image()

        full_img = self.screenshot(self.screen_region)
        self._draw_target_on_image(debug_img)

        offset_x = (self.screen[0] - self.fov[0]) // 2
        offset_y = (self.screen[1] - self.fov[1]) // 2 - self.offset - recoil_offset
        full_img[offset_y:offset_y+debug_img.shape[0], offset_x:offset_x+debug_img.shape[1]] = debug_img

        full_img = cv2.rectangle(
            full_img,
            (self.screen_center[0] - 5, self.screen_center[1] - 5),
            (self.screen_center[0] + 5, self.screen_center[1] + 5),
            (255, 255, 255),
            1
        )

        full_img = cv2.resize(full_img, self.window_resolution)
        cv2.imshow(self.window_name, full_img)
        cv2.waitKey(1)

    def _prepare_debug_image(self):
        """Prepare the thresholded image for debugging."""
        debug_img = cv2.cvtColor(self.thresh, cv2.COLOR_GRAY2BGR)
        return debug_img

    def _draw_target_on_image(self, debug_img):
        """Draw the detected target and other useful information on the debug image."""
        if self.target is not None:
            debug_img = cv2.line(
                debug_img,
                self.fov_center,
                (self.target[0] + self.fov_center[0], self.target[1] + self.fov_center[1]),
                (0, 255, 0),
                2
            )

        if self.closest_contour is not None:
            x, y, w, h = cv2.boundingRect(self.closest_contour)
            debug_img = cv2.rectangle(
                debug_img,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

        debug_img = cv2.rectangle(
            debug_img,
            (0, 0),
            (self.fov[0], self.fov[1]),
            (0, 255, 0),
            2
        )

        debug_img = cv2.rectangle(
            debug_img,
            (self.fov[0] // 2 - self.aim_fov[0] // 2, self.fov[1] // 2 - self.aim_fov[1] // 2),
            (self.fov[0] // 2 + self.aim_fov[0] // 2, self.fov[1] // 2 + self.aim_fov[1] // 2),
            (0, 255, 255),
            2
        )
