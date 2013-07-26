# Phone Sensors + WebSockets + Python

A quick experiment with WebSockets as a way to open up live phone sensor data to Python.

-----

## Components

* example-accel-client.html - The client side, meant to be run on the phone/devices. Opens up connection to server and hooks into the HTML5 device acceleration API to provide acceleration data.

* example-accel.py - The server side, which launches HTTP and WebSocket server instances and handles the streaming data.

* pywsock.py - A simple WebSockets server, adapted from [tanmaykm's pywebsock](https://gist.github.com/tanmaykm/5111225#file-pywebsock-py)

* simpleserver.py - HTTP server.

