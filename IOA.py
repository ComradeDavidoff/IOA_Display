#!/usr/bin/python

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1322
import time
from time import sleep
from PIL import ImageFont, Image, ImageDraw
from urllib.request import urlopen, Request
import urllib.request
import json
import requests
from textwrap3 import wrap
import textwrap
from pyquery import PyQuery
import math
import datetime
from lxml.html import fromstring
from lxml import html
import re

serial = spi(device=0, port=0)
device = ssd1322(serial)

# Define the font
font = ImageFont.truetype("/home/wackett/QVC/Roboto-Regular.ttf", 12)
splash_font = ImageFont.truetype("/home/wackett/QVC/Roboto-Regular.ttf", 22)

# Display splash screen
with canvas(device) as draw:
    draw.rectangle((0, 0, 255, 95), outline=0, fill=0)
    draw.text((10, 20), "QVC Item On-Air Display", font=splash_font, fill="white")
    sleep(5)

# Display the main content after the splash screen
# Main loop
while True:

    # Check if the connection to qvcuk.com is successful
    try:
        response = requests.get("https://www.qvcuk.com/")
        if response.status_code == 200:
            pass
        else:
            # Display a "please wait..." screen if the connection is not successful
            with canvas(device) as draw:
                draw.rectangle((0, 0, 255, 95), outline=0, fill=0)
                draw.text((10, 20), "Please wait, retrying...", font=splash_font, fill="white")
                sleep(30)
            continue
    except Exception as e:
        # Display a "please wait..." screen if there is an exception
        with canvas(device) as draw:
            draw.rectangle((0, 0, 255, 95), outline=0, fill=0)
            draw.text((10, 20), "Please wait, retrying...", font=splash_font, fill="white")
            sleep(30)
        continue

    # Fetch data from QVC website
    main_response = requests.get('https://www.qvcuk.com/ioa?channelCode=QVC')
    beauty_response = requests.get('https://www.qvcuk.com/ioa?channelCode=QBY')
    extra_response = requests.get('https://www.qvcuk.com/ioa?channelCode=QEX')
    style_response = requests.get('https://www.qvcuk.com/ioa?channelCode=QST')

    # Parse the HTML content
    main_tree = html.fromstring(main_response.content)
    beauty_tree = html.fromstring(beauty_response.content)
    extra_tree = html.fromstring(extra_response.content)
    style_tree = html.fromstring(style_response.content)

    # Extract item numbers
    main_item_numbers = main_tree.xpath('//*[@id="pageContent"]/div[1]/nav/div/div/div/ol/li[2]/text()')
    beauty_item_numbers = beauty_tree.xpath('/html/body/div[2]/div[1]/nav/div/div/div/ol/li[2]/text()')
    extra_item_numbers = extra_tree.xpath('/html/body/div[2]/div[1]/nav/div/div/div/ol/li[2]/text()')
    style_item_numbers = style_tree.xpath('/html/body/div[2]/div[1]/nav/div/div/div/ol/li[2]/text()')

    # Extract item descriptions
    main_description = main_tree.xpath('//*[@id="pageContent"]/div[3]/div[1]/div[2]/h1/text()')
    beauty_description = beauty_tree.xpath('//*[@id="pageContent"]/div[3]/div[1]/div[2]/h1/text()')
    extra_description = extra_tree.xpath('//*[@id="pageContent"]/div[3]/div[1]/div[2]/h1/text()')
    style_description = style_tree.xpath('//*[@id="pageContent"]/div[3]/div[1]/div[2]/h1/text()')

    # Get current date and time
    current_date = datetime.datetime.now().strftime("%d / %b")
    current_time = datetime.datetime.now().strftime("%H:%M")

    # Display information on OLED screen
    with canvas(device) as draw:
        # Clear the screen
        draw.rectangle((0, 0, 255, 95), outline=0, fill=0)

        # Display date
        draw.text((0, 0), current_date, font=font, fill="white")

        # Display title
        draw.text((110, 0), "Item On Air", font=font, fill="white")

        # Display time
        draw.text((220, 0), current_time, font=font, fill="white")

        # Display main channel information
        draw.text((0, 14), "Main:", font=font, fill="white")
        draw.text((45, 14), main_item_numbers[0], font=font, fill="white")
        draw.text((92, 14), main_description[0], font=font, fill="white")

        # Display extra channel information
        draw.text((0, 26), "Extra:", font=font, fill="white")
        draw.text((45, 26), extra_item_numbers[0], font=font, fill="white")
        draw.text((92, 26), extra_description[0], font=font, fill="white")

        # Display style channel information
        draw.text((0, 38), "Style:", font=font, fill="white")
        draw.text((45, 38), style_item_numbers[0], font=font, fill="white")
        draw.text((92, 38), style_description[0], font=font, fill="white")

        # Display beauty channel information
        draw.text((0, 50), "Beauty:", font=font, fill="white")
        draw.text((45, 50), beauty_item_numbers[0], font=font, fill="white")
        draw.text((92, 50), beauty_description[0], font=font, fill="white")

        sleep(60)  # Delay of one minute between updates

