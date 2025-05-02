**This project is free and open-source. I am a student who spends their free time on this project. If you like the project and want its development to continue:**  
** [Donate](https://github.com/vike256#donate)**  
** Give a star**  

---

<img src=https://i.imgur.com/c55L14T.png alt="Unibot logo" width="250">  

# 143X (Upgraded Unibot by DXXTHLY)

**143X** is a modernized, feature-extended version of the original [Unibot](https://github.com/vike256/Unibot) colorbot, upgraded and maintained by [DXXTHLY](https://github.com/dxxthly).  
It is a multi-functional assistant tool developed for PC shooter games, with focus on educational use and experimentation in Python-based automation and color detection.

It simulates mouse input using various methods:  
- **Windows `mouse_event` functions**
- **Interception driver**
- **External hardware** capable of simulating HID input (Arduino Leonardo, Raspberry Pi Pico, etc.)

143X can communicate with these devices over COM ports or socket connections (Ethernet/Wi-Fi).

---

##  What's New in 143X?

- Cleaner, modular code
- Reloadable config at runtime
- Rapid-fire mode added
- More consistent recoil mitigation
- Flexible keybinds and toggles
- Improved debug tools

---

##  Key Features

###  Aim Assist
- Detects enemies using pixel color ranges (HSV)
- Smoothly moves crosshair toward the target

###  Triggerbot
- Fires automatically when your crosshair is over a target

###  Rapid-fire
- Simulates fast semi-auto fire using automatic clicks

###  Recoil Mitigation
- Helps control weapon spray patterns
- Supports both **point-and-shoot** and **offset recoil** behavior

---

**Showcase video:**  
<a href="https://youtube.com/watch?v=8LUBfXCIu6I" target=_blank><img src="https://i.imgur.com/tNO8ZMF.png" alt="Showcase video thumbnail" width="600"></a>    
[*Python colorbot hits world record 220k+ score with 100% accuracy on Aim Lab*](https://youtube.com/watch?v=8LUBfXCIu6I)

---

##  Installation & Usage

Check the [Wiki Guide](https://github.com/vike256/Unibot/wiki/Guide)  
> (Note: 143X includes additional hotkeys and settings not reflected in the original Unibot wiki)

---

##  Disclaimer

This is a **hobby project**, maintained by [DXXTHLY](https://github.com/dxxthly), and is **intended for educational purposes only**.  

> I do **not condone** cheating in online games.  
> If you’re using this to cheat, consider the impact on others and ask yourself why. Cheating ruins the experience for everyone, including yourself.

---

##  Credits

- Original Project: [vike256](https://github.com/vike256)
- Upgrade & Maintenance: [DXXTHLY](https://github.com/dxxthly)

---

##  License

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
