import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import os
import time

WIDTH = 128
HEIGHT = 64
BORDER = 5
FONT_SIZE = 12

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

oled.fill(0)
oled.show()

image = Image.new("1", (WIDTH, HEIGHT))

draw = ImageDraw.Draw(image)

font = ImageFont.load_default()

def get_cpu_temperature():
    return float(os.popen('vcgencmd measure_temp').readline().replace("temp=","").replace("'C\n",""))

def get_ram_usage():
    total_mem = os.popen('free -m | grep Mem').readline().split()[1]
    used_mem = os.popen('free -m | grep Mem').readline().split()[2]
    return round((int(used_mem) / int(total_mem)) * 100, 2)

def get_wifi_ssid():
    wifi_ssid = os.popen('iwgetid -r').read().strip()
    if not wifi_ssid:
        return "RASPI"
    return wifi_ssid

t = time.time()
while True:
    if time.time() - t > 5:
        t = time.time()
        wifi_ssid = get_wifi_ssid()
        ip_address = os.popen('hostname -I').read().strip()
        cpu_temp = get_cpu_temperature()
        ram_usage = get_ram_usage()
        
        draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)  # Clear the display
        
        if not ip_address:  # Check if ip_address is empty
            draw.text((BORDER + 5, BORDER + 5), "No Network", font=font, fill=255)
            draw.text((BORDER + 5, BORDER + 5 + 1 * FONT_SIZE), "Press Setup Button", font=font, fill=255)
        else:
            if wifi_ssid == "RASPI":
                draw.text((BORDER + 5, BORDER + 5), "Hotspot: "+wifi_ssid, font=font, fill=255)
            else:
                draw.text((BORDER + 5, BORDER + 5), "WiFi: "+wifi_ssid, font=font, fill=255)
        
            draw.text((BORDER + 5, BORDER + 5 + 1 * FONT_SIZE), "IP: "+ip_address, font=font, fill=255)
        draw.text((BORDER + 5, BORDER + 5 + 2 * FONT_SIZE), f"CPU Temp: {cpu_temp}C", font=font, fill=255)
        draw.text((BORDER + 5, BORDER + 5 + 3 * FONT_SIZE), f"RAM Usage: {ram_usage}%", font=font, fill=255)
        
        oled.image(image)
        oled.show()
