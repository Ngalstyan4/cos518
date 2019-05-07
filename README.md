# cos518

To run the network simulation, just run
```bash
sudo python cos518network.py
```

This simulates a network with a topology defined in the python file
The python file also specifies the web server application that is going to run on each simulated node.
In our case this server is defined in [`flask_app.py`](flask_app.py)

The server as of now is just a wrapper around [`hyperbolic.py`](hyperbolic.py) that exposes its `get` and `put` functions as network apis

The server runs on the dedicated ip and port 3000 on all virtual nodes.
After running mininet, to get a key, run
```
curl IP:3000/[key]
```
To put a key, run:
```
curl -X PUT -d "value=valueUnderKey&cost=44" IP:3000/[key]
```

Note that both value and cost are optional. A value of `None` and a cost of 0 will be passed to the cache api if these values are not provided
