#!/usr/bin/env python

import requests
import json
import turtle
import time


__author__ = 'ElizabethS5'


def get_astronauts():
    """Prints astronauts full names and the spacecraft they are currently on board.
    Prints the total number of astronauts in space."""
    response = requests.get('http://api.open-notify.org/astros.json')
    json_data = json.loads(response.text)
    people = json_data['people']
    number = json_data['number']
    for person in people:
        print(f'{person["name"]} is aboard the {person["craft"]}.')
    print(f'There are currently {number} astronauts in space.')


def get_location():
    """Prints the current time and geographic coordinates (lat/lon) of the
    space station. Returns longitude and latitude tuple."""
    response = requests.get('http://api.open-notify.org/iss-now.json')
    json_data = json.loads(response.text)
    position = json_data['iss_position']
    timestamp = json_data['timestamp']
    print(
        f"{time.ctime(timestamp)}: ISS is at latitude {position['latitude']}"
        + f" and longitude {position['longitude']}."
    )
    return (float(position['longitude']), float(position['latitude']))


def use_turtle(lon, lat):
    """Makes instance of turtle. Coordinates its setup and actions."""
    iss_turtle = turtle.Turtle()
    set_up_screen(iss_turtle)
    set_up_turtle(iss_turtle)
    mark_indy(iss_turtle)
    go_to_current_location(iss_turtle, lon, lat)
    turtle.done()


def set_up_screen(turt):
    """Creates a graphics screen with the world map background image."""
    turt.screen.bgpic('./map.gif')
    turt.screen.setup(width=720, height=360, startx=0, starty=0)
    turt.screen.setworldcoordinates(-180, -90, 180, 90)
    turt.screen.title("ISS Location")


def set_up_turtle(turt):
    """Registers an icon image for the ISS station within the turtle screen
    context."""
    turt.screen.register_shape('iss.gif')
    turt.hideturtle()
    turt.shape('iss.gif')
    turt.setheading(0)
    turt.penup()


def mark_indy(turt, indy_lat=39.7681, indy_lon=-86.1581):
    """Plots a yellow dot on the map at Indy's lat/long.  Renders the next
    passover time next to the Indianapolis location dot"""
    turt.goto(indy_lon, indy_lat)
    turt.dot(2, "yellow")
    turt.forward(2)
    turt.pencolor('yellow')
    turt.write(when_over_location(indy_lat, indy_lon))


def go_to_current_location(turt, lon, lat):
    """Moves the ISS station to its current lat/lon on the map."""
    turt.goto(lon, lat)
    turt.showturtle()


def when_over_location(lat, lon):
    """Prints and returns the next time that the ISS will be over
    Indianapolis, IN."""
    response = requests.get(
        'http://api.open-notify.org/iss-pass.json',
        params={
            "lat": lat,
            "lon": lon
        })
    json_data = json.loads(response.text)
    risetime = time.ctime(json_data['response'][0]['risetime'])
    print(f'{risetime} is the next time ISS will be over Indianapolis, IN.')
    return risetime


def main():
    """Calls functions that make API get requests about ISS and uses
    information and with turtle graphics library"""
    get_astronauts()
    use_turtle(*get_location())


if __name__ == '__main__':
    main()
