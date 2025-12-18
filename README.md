# Nishan's Hackpad
This is my hackpad, which will boost my productivity by a heap.

## What my hackpad offers
- 14 completely programmable keys
- 1 rotary encoder
- An oled screen(128*32)
- Per key rgb(SK6812 MINI-E led is used)

## CAD
My case is a bit complex because I wanted to side mount the oled screen. My case assembly would have 4 parts in total. One is the main body, another one is the bottom plate, another one is a side holder for oled screen and the last one is key plate. The bottom plate fits in place with the main body using a snap fit feature. the top key plate isn't directly attached to the body yet. I think keeping that free, laying over the body won't hurt. And for the side holder that holds the oled screen, I will stick it to the main body using superglue. The parts are shown below!
Full Assembly   |   Case without components   | Main Body   |   Bottom Plate | Side Holder | Key Plate
:------------:|:------------:|:------------:|:------------:|:------------:|:------------:|
![](https://github.com/Nishan-wisdomadventure/Nishan-s-Hackpad/blob/main/Hackpad_Images/Cad_Images/Screenshot%20from%202025-12-19%2001-36-05.png) | ![](https://github.com/Nishan-wisdomadventure/Nishan-s-Hackpad/blob/main/Hackpad_Images/Cad_Images/Screenshot%20from%202025-12-19%2001-52-31.png) | ![](https://github.com/Nishan-wisdomadventure/Nishan-s-Hackpad/blob/main/Hackpad_Images/Cad_Images/Screenshot%20from%202025-12-19%2001-37-05.png) | ![](https://github.com/Nishan-wisdomadventure/Nishan-s-Hackpad/blob/main/Hackpad_Images/Cad_Images/Screenshot%20from%202025-12-19%2001-37-15.png) | ![](https://github.com/Nishan-wisdomadventure/Nishan-s-Hackpad/blob/main/Hackpad_Images/Cad_Images/Screenshot%20from%202025-12-19%2001-37-41.png) | ![](https://github.com/Nishan-wisdomadventure/Nishan-s-Hackpad/blob/main/Hackpad_Images/Cad_Images/Screenshot%20from%202025-12-19%2001-38-10.png) |


## PCB
Designing the pcb and exporting it was the most exhausting thing! Again, this is because my laptop can't handle kicad so I had to use easyeda. Here are schematics and screenshots of the pcb!
Schematic   |   PCB |
:-----------:|:-----------:|
![](https://github.com/Nishan-wisdomadventure/Nishan-s-Hackpad/blob/main/Hackpad_Images/PCB_Images/PCB_SVG.svg) | ![](https://github.com/Nishan-wisdomadventure/Nishan-s-Hackpad/blob/main/Hackpad_Images/PCB_Images/Screenshot%20from%202025-12-19%2002-04-46.png)


## Firmware
The firmware is written in kmk. Not much is added right now, I am gonna experiment and add new things when I get the hackpad in my hands!

## BOM
| ID | Name                                         | Quantity |                |
|----|----------------------------------------------|----------|----------------|
| 1  | OLED DISPLAY 128x32 0.91"" I2C | 1        |                |
| 2  | SK6812 MINI-E                                | 16       |                |
| 3  | MX-Style switches                             | 14       |                |
| 4  | EC11 Rotary encoders                         | 1        |                |
| 5  | Seeed XIAO RP2040                            | 1        |                |
| 6  | 74HC595A Shift Register                                     | 1        | (Self Sourced) |
| 7  | Through-hole 1N4148 Diodes                                       | 15       |                |