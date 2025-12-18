import board
import digitalio
import busio
import time
import supervisor
import adafruit_ssd1306
import neopixel
from kmk.keys import KC, make_consumer_control_key
from kmk.matrix import MatrixScanner
from kmk.platform import platform
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderModule
from kmk.scanners import DiodeOrientation

# Hardware pins
ROWS = (board.D0, board.D1, board.D2)
DS_PIN = board.D3
SHCP_PIN = board.D6
STCP_PIN = board.D7
ENC_A = board.D9
ENC_B = board.D10

# OLED I2C pins
I2C_SDA = board.D4
I2C_SCL = board.D5

# LEDs
LED_PIN = board.D8
LED_COUNT = 16

# Matrix
COL_COUNT = 5
ROW_COUNT = 3

# --- Shift register keyboard matrix ---
class ShiftRegMatrix(MatrixScanner):
    def __init__(self, rows, ds_pin, shcp_pin, stcp_pin):
        super().__init__(DiodeOrientation.COL2ROW)
        self.rows = [digitalio.DigitalInOut(p) for p in rows]
        for row in self.rows:
            row.direction = digitalio.Direction.INPUT
            row.pull = digitalio.Pull.UP

        self.ds = digitalio.DigitalInOut(ds_pin)
        self.shcp = digitalio.DigitalInOut(shcp_pin)
        self.stcp = digitalio.DigitalInOut(stcp_pin)
        self.ds.direction = digitalio.Direction.OUTPUT
        self.shcp.direction = digitalio.Direction.OUTPUT
        self.stcp.direction = digitalio.Direction.OUTPUT
        self.ds.value = False
        self.shcp.value = False
        self.stcp.value = False

    def matrix_scan(self):
        matrix_state = [0] * (ROW_COUNT * COL_COUNT)
        for col in range(COL_COUNT):
            pattern = 0x1F ^ (1 << col)
            for bit in range(7, -1, -1):
                self.ds.value = bool(pattern & (1 << bit))
                self.shcp.value = True
                self.shcp.value = False
            self.stcp.value = True
            self.stcp.value = False
            for row in range(ROW_COUNT):
                if not self.rows[row].value:
                    matrix_state[row * COL_COUNT + col] = 1
        return matrix_state

# --- LED Setup ---
leds = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=0.2, auto_write=True)

# LED breathing animation parameters
breath_step = 0
breath_dir = 1
BREATH_MIN = 0.05
BREATH_MAX = 0.2

def led_breathe():
    global breath_step, breath_dir
    brightness = BREATH_MIN + (BREATH_MAX - BREATH_MIN) * (0.5 * (1 + math.sin(breath_step)))
    leds.brightness = brightness
    color = (0, 150, 255)  # light blue
    leds.fill(color)
    breath_step += 0.05
    if breath_step > 2 * math.pi:
        breath_step -= 2 * math.pi

# --- OLED Setup ---
i2c = busio.I2C(I2C_SCL, I2C_SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# OLED key log
key_log = []

def update_oled(layer_name, key_label):
    global key_log
    if key_label:
        key_log.append(key_label)
        if len(key_log) > 3:
            key_log.pop(0)
    oled.fill(0)
    oled.text(f"Layer:{layer_name}", 0, 0, 1)
    oled.text(" ".join(key_log), 0, 16, 1)
    oled.show()

# --- Encoder ---
MINS = make_consumer_control_key(0x2A1)  # Minimize
encoder = EncoderModule(
    pin_a=ENC_A,
    pin_b=ENC_B,
    pin_button=ROWS[2],
    encoder_map=[(KC.MEDIA_VOLUME_UP, KC.MEDIA_VOLUME_DOWN)],
    button_map=[MINS]
)

# --- Layers ---
layers = Layers()

# --- Keymap ---
keymap = [
    [KC.Q, KC.W, KC.E, KC.R, KC.LSFT,
     KC.A, KC.S, KC.D, KC.F, KC.LCTL,
     KC.Z, KC.X, KC.C, KC.V, KC.B],
    [KC.N1, KC.N2, KC.N3, KC.N4, KC.RAISE,
     KC.N6, KC.N7, KC.N8, KC.N9, KC.N0,
     KC.MINS, KC.EQL, KC.BSPC, KC.LGUI, KC.LALT]
]

# --- Matrix ---
matrix = ShiftRegMatrix(ROWS, DS_PIN, SHCP_PIN, STCP_PIN)

# --- Keyboard init ---
keyboard = platform.keyboard(
    matrix=matrix,
    keymap=keymap,
    modules=[layers, encoder],
    debug_enabled=True
)

# Map KC -> short names for OLED
key_labels = {
    KC.Q: "Q", KC.W: "W", KC.E: "E", KC.R: "R", KC.LSFT: "Shft",
    KC.A: "A", KC.S: "S", KC.D: "D", KC.F: "F", KC.LCTL: "Ctrl",
    KC.Z: "Z", KC.X: "X", KC.C: "C", KC.V: "V", KC.B: "B",
    KC.N1: "1", KC.N2: "2", KC.N3: "3", KC.N4: "4", KC.RAISE: "RSE",
    KC.N6: "6", KC.N7: "7", KC.N8: "8", KC.N9: "9", KC.N0: "0",
    KC.MINS: "-", KC.EQL: "=", KC.BSPC: "BS", KC.LGUI: "GUI", KC.LALT: "ALT",
}

# Override keyboard method to update OLED on key press
original_send_key = keyboard.send_key

def send_key_override(*args, **kwargs):
    key = args[0] if args else None
    layer_name = f"{keyboard.active_layers[-1]}"
    label = key_labels.get(key, None)
    update_oled(layer_name, label)
    return original_send_key(*args, **kwargs)

keyboard.send_key = send_key_override

# --- Main loop ---
import math
if __name__ == "__main__":
    while True:
        led_breathe()
        keyboard.go()  # KMK main loop

