# Akenasai

For an old small project, I used a Raspberry Pi to remotely open my garage door. The Raspberry had a XML-RCP server running on my Wifi using `python`'s `SimpleXMLRPCServer`. When requested, the Raspberry simulated a physical button press using a relay-switch circuit ([examples](https://www.electronics-tutorials.ws/blog/relay-switch-circuit.html)) directly connected to the two sides of a physical button located behind the door.

To perfom the request, I created an Android application using the [`kivy framework`](https://kivy.org/) for the user interface, [`jnius`](https://pyjnius.readthedocs.io/en/stable/) to access the Wifi functions of the phone, and [`buildozer`](https://buildozer.readthedocs.io/en/latest/) for packaging the python application for my Android phone (for this step, I mostly followed the [official kivy instructions](https://kivy.org/doc/stable/guide/packaging-android.html)).

This repository contains the code for the Android application and the XML-RCP client. The server part is missing and may be added at some point.

Note: Akenasai (開けなさい) means "open yourself" in Japanese.