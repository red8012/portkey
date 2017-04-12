# Portkey

A Python framework for interacting with in-browser DOM via websockets.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Description](#description)
  - [Motivation](#motivation)
  - [How it works](#how-it-works)
  - [Limitations](#limitations)
  - [Recommended Usage](#recommended-usage)
- [Dependencies](#dependencies)
- [Installation](#installation)
  - [Automatic](#automatic)
  - [Manual](#manual)
- [Usage](#usage)
    - [Step 1](#step-1)
    - [Step 2](#step-2)
    - [Step 3](#step-3)
    - [Step 4](#step-4)
- [Documentation and Examples](#documentation-and-examples)
- [Performance](#performance)
- [Status](#status)
- [Todo](#todo)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Description

### Motivation

From time to time, people ask me how to make a **GUI** for their Python program. I am somewhat reluctant to recommend toolkits like TkInter, Qt or GTK. For most people, it is easier to make a fancy UI with web technology than with traditional GUI toolkits because there are so many sophisticated frameworks, libraries, and tools in the web ecosystem for making a great frontend. 

However, to let a Python program communicate with a web page, one must do a lot of tedious work packing/unpacking/sending/receiving data via AJAX or something like that. By this way, the code usually ends up being half in Python and half in Javascript no matter what framework is chosen, making it a bad choice to use a web page as an alternative to a traditional GUI.

To make life easier, I make Portkey for taking care of the communication between a Python backend and a web frontend. From now on, building GUI in HTML & CSS becomes a viable solution for Python. 

### How it works

Portkey is still using a server-client model. Your Python program running Portkey framework is the server, and the web pages execute `portkey.js` are clients.

When a client loads, it tries to connect to your Portkey server via websocket. Once connected and the DOM is ready, it informs the server and the server tells it to bind events registered in your Python code.

The following things happen every time a registered event fired on the DOM (e.g. clicking on a button).

1. The client packs the corresponding handler function ID along with data required in the  `with_ui_data` decorator and sends them to the server.
2. The server executes the handler coroutine function to react to the event and send commands instructing the client to update the UI.
3. The client does DOM manipulations according to the response from the server.

### Limitations

* Due to the cost of sending messages between the browser and your Python program, the response time is expected to be quite a bit slower than native GUI toolkits. However, if you don't mind the extra latency of few milliseconds, it should still be a feasible solution.
* Although it mimics jQuery behavior in Python language, it does not guarantee everything works. Selectors, events, dimensions, effects and manipulations should mostly work while functions of other categories may not work.



### Recommended Usage

Portkey is meant to be used as a tool to build a GUI program running on your computer or inside a container. It is NOT a generic backend framework. Please avoid exposing it on the Internet.



## Dependencies

* Python 3.6 or above
* [Websockets](https://websockets.readthedocs.io/en/stable/)
* [Werkzeug](http://werkzeug.pocoo.org)
* [jQuery](http://jquery.com)
* A **modern** browser
* [Dominate](https://github.com/Knio/dominate) (optional, but highly recommended)



## Installation

### Automatic

```sh
pip install portkey
```

### Manual

```sh
git clone https://github.com/red8012/portkey.git
cd portkey
python setup.py install
```



## Usage

After installing Portkey, you can write your first Portkey program using the boilerplate below.

#### Step 1

Make an empty directory `myPortkeyProject/` , copy `portkey.js` from this repository to the directory.

#### Step 2

Save the following code as `myPortkeyProject/starter.html`.

```html
<!DOCTYPE html>
<html>
    <body>
        <button id="btn">button</button>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
        <script src="portkey.js"></script>
    </body>
</html>
```

#### Step 3

Save the following code as `myPortkeyProject/starter.py`.

```Python
from portkey import *

@onclick('#btn')
async def on_click_btn1(s, d, c):
    s('#btn').text('clicked')

start_app()
```

#### Step 4

Run `python starter.py` under myPortkeyProject directory. Open `starter.html` in your browser. Try clicking on the button, the text on it should become *clicked*.

## Documentation and Examples

To get more instructions and useful examples, please clone and run `python examples/example.py` in this repository and open `examples/example.html` in the browser to see interactive examples.

## Performance

Portkey focuses on convenience, not performance. However, it is still possible to do more than 2000 round-trip communications per second between the server and the client (on localhost). It should be sufficient for non-realtime usage.

You can benchmark it by launching `examples/performanceTest.py` and `examples/performanceTest.py`.

## Status

* This framework is at pre-alpha stage. Use it at your risk.
* Any kind of contributions is welcome. Please report issues and/or send PR to me if you found something broken.



## Todo

* Tests, tests, tests.
* Docs, docs, docs.

