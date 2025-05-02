**This project is free and open-source. I am a student who spends their free time on this project. If you like the project and want its development to continue:**  
** [Donate](https://github.com/dxxthly#donate)**  
** Give a star**  

---

<img src="https://i.imgur.com/c55L14T.png" alt="143X logo" width="250">  

# 143X  
### *(An upgraded Unibot fork by [DXXTHLY](https://github.com/dxxthly))*

**143X** is a modern, customizable Python-based **colorbot** designed for FPS games, forked and upgraded from [Unibot](https://github.com/vike256/Unibot).  
It combines pixel detection, automated mouse input, and real-time control to simulate aim-assist mechanics — intended **for educational and experimentation purposes only**.

> This tool showcases how computer vision, OpenCV, and basic input simulation can work together to form intelligent automation for games.

---

##  What's New in 143X?

-  Live config reloading (no restarts!)
-  Fully implemented Rapid-Fire mode
-  Toggle hotkeys for Aim & Recoil assist
-  Cleaner modular Python code
-  Enhanced debug & screen masking
-  More precise recoil patterns
-  Fully adjustable color detection + FOV

---

##  Key Features

### Aimbot
- HSV color-based pixel detection for enemy spotting
- Configurable smoothness, speed, offset, and height control
- Adjustable FOV for fine-tuned aim windows

###  Triggerbot
- Instantly fires when your crosshair lands on a detected target
- Configurable trigger delay + randomization options

###  Rapid-Fire
- Auto-clicker for burst and semi-auto weapons
- Customizable click rate (CPS)

###  Recoil Control
- Simulates drag-down recoil compensation
- Supports multiple recoil styles (including offset-based)

---

** Showcase video:**  
<a href="https://youtube.com/watch?v=8LUBfXCIu6I" target="_blank"><img src="https://i.imgur.com/tNO8ZMF.png" alt="Showcase video thumbnail" width="600"></a>  
[*Python colorbot hits world record 220k+ score with 100% accuracy on Aim Lab*](https://youtube.com/watch?v=8LUBfXCIu6I)

---

##  Installation & Usage

See the [original Unibot Wiki](https://github.com/vike256/Unibot/wiki/Guide) for detailed setup steps.  
143X introduces new hotkeys and config options not yet documented in that guide.  
**For new keybinds and settings, refer to `config.ini` in this repo.**

---

##  Compatibility

143X supports input simulation via:

-  Windows `mouse_event` API (default)
-  Interception driver (kernel-level input)
-  External devices via COM or Socket (Arduino Leonardo, RP Pico, etc.)

Switch modes via `[communication]` in `config.ini`.

---

##  Disclaimer

This project is for **educational purposes only.**  
Cheating in multiplayer games is unethical and devalues real competition.  
If you use this for anything beyond learning or offline play — ask yourself why.

---

##  Credits

- **Original Author**: [vike256](https://github.com/vike256)
- **Upgraded and Maintained by**: [DXXTHLY](https://github.com/dxxthly)

> Big respect to vike256 for releasing Unibot under the GPL and inspiring future developers.

---

## 📄 License

```text
143X (Upgraded Unibot), an open-source colorbot.  
Originally created by vike256.  
Upgraded and maintained by DXXTHLY (2025).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
