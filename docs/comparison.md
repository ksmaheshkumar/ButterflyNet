### Still not convinced?

Here's a quick comparison between networking libraries.



Pure sockets:
```python
#!/usr/bin/env python 

""" 
A simple echo server 
""" 
import socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind(('0.0.0.0', 5000)) 
s.listen(5)
while 1: 
    client, address = s.accept() 
    data = client.recv(1024) 
    if data: 
        client.send(data) 
    client.close()
```

Twisted: (taken from https://twistedmatrix.com/documents/current/_downloads/simpleserv.py)

```python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
from twisted.internet import reactor, protocol

class Echo(protocol.Protocol):    
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        self.transport.write(data)

def main():
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8000,factory)
    reactor.run()

if __name__ == '__main__':
    main()
```

asyncio:

```python
import asyncio
@asyncio.coroutine
def handle_echo(reader, writer):
    data = yield from reader.read(100)
    writer.write(data)
    yield from writer.drain()
    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
```



