import machine
import network
import utime
from display import LCD_1inch3
from urequests import request


def call_flask(path):
    r = request("GET", f"http://<ip-of-the-flask-server>:5000/{path}")
    return r.json()


def show_text(string):
    display.fill(0)
    display.text(string, 1, 1, display.white)
    display.show()


def show_state(state):
    if result.get("start") and result.get("stop") is None:
        show_text("started: " + result["start"])
    else:
        show_text("no entry started")


# connect to wifi
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect("wifi-ssid", "wifi-password")

# init display
display = LCD_1inch3()
display.fill(0)
display.show()

button_a = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
once = True

# show initial state when started
result = call_flask("state")
show_state(result)

while True:
    # check for button press + release
    button_a_press = button_a.value()
    utime.sleep_ms(10)
    button_a_release = button_a.value()

    if button_a_press and not button_a_release and once:
        once = False
        result = call_flask("toggle")
        show_state(result)
    elif not button_a_press and button_a_release:
        once = True
