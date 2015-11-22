# Simple Chat Server

Here, we'll be creating something a bit more advanced than a simple TCP echo server. This will be a chat server, that 
accepts multiple clients, and forwards messages from each client to the other client.

## The Handler

As usual, we need to get a new ButterflyHandler before we do anything. However, this time, we want to write our own 
handler with overriden methods for `on_connection` and `on_disconnect`, allowing us to send messages to the other 
clients connected about new people joining the room.

First, we begin with the standard imports and code for any ButterflyNet usage.

    import asyncio
    from bfnet import ButterflyHandler
    
    loop = asyncio.get_event_loop()
    
Next, we subclass ButterflyHandler to get our own custom handler.

    class MyHandler(ButterflyHandler):
        @asyncio.coroutine
        def on_connection(butterfly):
            pass
        
        @asyncio.coroutine
        def on_disconnect(butterfly):
            pass
            
These two methods are crucial - they are automatically called when the butterfly connects, or when it disconnects. In
 a vanilla handler, they do basic things such as setting up and running your data handlers in a loop, and stopping 
 your data handler. 
 
## `on_connection`

`on_connection` is called when a new client is created. The `butterfly` parameter is the butterfly that was just 
created recently, and you can read from/write to it. Right now, all it is doing is feeding data into it's internal 
buffer for usage in your application.  

The default `on_connection` simply begins your handler loop, and adds the butterfly to the internal dictionary of 
butterflies, based on it's IP and port which (should) be unique.

However, we want to override this to get the nickname from the client that is connecting, and use that for storing 
the butterflies.

First, we tell the user to enter their name:

    butterfly.write(b"Username: ")
    
Next, we read in the username sent.

    nick = yield from butterfly.read().replace(b'\r', b"").replace(b'\n', b"")
    self.logger.debug("{} has joined".format(nick.decode()))
    
This also replaces any newline characters in their username with nothing.

Then, we notify all the other butterflies of the new user.
  
-------

In a ButterflyHandler, there is a structure of every Butterfly connected to your server, stored in the dictionary 
`butterflies`. This is a key-value mapping of something unique about the Butterfly, by default the "ip:port" is the 
key, but it can be any string value. In this, we will use the nickname as the string value.
The value of an item in this structure is a tuple: `(butterfly, handler_fut)`.

   - The Butterfly object is the first item, and is used by anything else that needs to access the client object in 
    a different handler.
   - The handler_fut object is the Future referring to the handler infinite loop for that Butterfly. This is 
    typically accessed by a disconnect routine, that cancels the Future and terminates the connection.
    
To tell the other butterflies, we simply loop over the items of this dict:
    
    for butterfly, _ in self.butterflies.values():
        butterfly.write(nick + b" has joined the room.")
   
------
   
Next, we want to save the nick somewhere we can access it later, for usage in our handler.

    butterfly.nick = nick
    
We then run our `Net.handle` in a Task inside the event loop, meaning we can now begin handling the data.
    
    fut = self.begin_handling(butterfly)
    
Finally, we save the Butterfly/Handle pair in the butterfly dictionary.

    self.butterflies[nick] = (butterfly, fut)
    
Our final code will look something like this:

    @asyncio.coroutine
    def on_connection(self, butterfly: Butterfly):
        butterfly.write(b"Nickname: ")
        nick = yield from butterfly.read().replace(b'\r', b'').replace(b'\n', b'')
        self.logger.debug("{} has joined".format(nick.decode()))
        for bf, _ in self.butterflies.values():
            bf.write(nick + b" has joined the room\n")
        butterfly.nick = nick.
        fut = self.begin_handling(butterfly)
        self.butterflies[nick] = (butterfly, fut)
    
## `on_disconnect`
    
Our disconnect method is equally as important as the on_connection method, as it tells all the other butterflies the 
user has left the room, and cancels processing of any new data from the disconnected client.

-------
    
First, we need to make sure they entered a nick and connected to the server cleanly.

        if not hasattr(butterfly, "nick"):
            self.logger.warning("Connection cancelled before on_connect finished!")
            return

Then, we get the handler Future from the dictionary of Butterflies.

    bf = self.butterflies.pop(butterfly.nick)
    
We cancel the Future, preventing any more handling from taking place.

    bf[1].cancel()
    
Finally, we tell everybody else that the client has disconnected.

    for bf, _ in self.butterflies.values():
        bf.write(butterfly.nick + b" has left the room.\n")
        
The final code:

    @asyncio.coroutine
    def on_disconnect(self, butterfly: Butterfly):
        if not hasattr(butterfly, "nick"):
            self.logger.warning("Connection cancelled before on_connect finished!")
            return
        bf = self.butterflies.pop(butterfly.nick)
        bf[1].cancel()
        for bf, _ in self.butterflies.values():
            bf.write(butterfly.nick + b" has left the room.\n")

## Handling messages

Similarly to our echo server, we now need to handle messages from our connected clients. First, we start by getting a
 reference to the server in our main method:
 
    @asyncio.coroutine
    def main():
        my_handler = MyHandler.get_handler(loop=loop, log_level=logging.DEBUG)
        my_server = yield from my_handler.create_server(("127.0.0.1", 8001), ("localhost.crt", "server.key", None))
        
Then we define a coroutine for handling our messages.

    @my_server.any_data
    @asyncio.coroutine
    def handle_data(data: bytes, butterfly: Butterfly, handler: ButterflyHandler):
    
Next, we simply loop over the list of butterflies we had earlier, sending them the same message that we just recieved.

    for bf in handler.butterflies.values():
        if bf[0] != butterfly:
            bf[0].write(butterfly.nick + b": " + data)

Make sure to check you're not sending the message to yourself, by checking bf[0] is not you.

