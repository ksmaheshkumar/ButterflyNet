# Starting with ButterflyNet

The first thing to do when learning a new networking framework is to write a simple TCP Echo server.

-------

### Imports
__First, import the required modules.__


    import asyncio
    import bfnet
   

Importing `asyncio` allows you to create coroutines for use inside bfnet, and importing `bfnet` 
allows you to access all the ButterflyNet classes.
  
You will also want to create an event loop for the server to use. The event loop is key 
to everything - all your code runs off this loop.

    loop = asyncio.get_event_loop()

-------

### The ButterflyHandler

__Next, you create a new Handler.__ 

Typically you would:  

 - Subclass ButterflyHandler (`class MyHandler(ButterflyHandler`), and add your own methods
 - Store this in a separate class so all your business logic can grab an instance of the class when required.
 
However, this is not required for this tutorial as it is a simple one-file example.  

A `ButterflyHandler` is a class that handles butterflies (who would've guessed?). It is responsible for 
creating new ones when a client connects, handling what happens when a client connects or disconnects, 
and managing the list of butterflies that are connected to the server.

Creating the handler is simple: 

    my_handler = bfnet.get_handler(loop)

-------

### Creating a Net

A Net is the core of your ButterflyNet application. It catches the connecting Butterflies and handles their
data.

The net creation is handled by your ButterflyHandler. It will setup your SSL connection, create a new Butterfly
factory and handle your incoming data.

To create a new one, it's another call to your handler:

    my_server = yield from my_handler.create_server(("127.0.0.1", 8001), ("my_server.crt", "m_server.key", None))

Here's a breakdown of the arguments:  

 - The first argument is a tuple containing the address and port to bind to. Here, 
 we bind it to the loopback interface (localhost) and port 8001.
 - The second argument is a tuple of data about the SSL data.
   This uses a keypair called `my_server.crt/.key`, and no private key password (specified by the `None`).  
   See [here](https://www.digitalocean.com/community/tutorials/openssl-essentials-working-with-ssl-certificates-private-keys-and-csrs) 
   for more information about certificate generation.
   
However, because this is a `yield from` method, we have to run it inside our own function. 
    
    @asyncio.coroutine
    def main():
        my_server = yield from my_handler.create_server(("127.0.0.1", 8001), ("my_server.crt", "m_server.key", None))
        

------
   
### Our data handler
In ButterflyNet, every single byte of data that is pulled into the Butterfly is sent to a StreamReader, 
which is then pulled every time a handler for the most previous set of data has returned.  
An infinite loop inside your Net will call your application-side handlers automatically, in order of when they were added.  

Here, we add a very simple data handler that just tells the server to echo everything that is sent.

This handler must also be inside your `main()` function, otherwise you cannot access the server object.

    @my_server.any_data
    @asyncio.coroutine
    def echo(data, butterfly, handler):
        butterfly.write(data)

-------

Let's go through this line by line.  

`@my_server.any_data` - This decorator tells the Net to call your handler on ANY data that is sent.
No checking takes place on what comes down the line.  
`@asyncio.coroutine` - This decorator makes your function a coroutine - an asynchronous function. 
This is required for all handlers and most user-overridable methods.  
`def echo(data, butterfly, handler):` - This creates a new function with the required parameters for the handler.

 - Data is the data recieved.
 - Butterfly is the butterfly object created.
 - Handler is your ButterflyHandler you created earlier.

`butterfly.write(data)` - This actually echos the data to the butterfly, by writing back exactly what was said.

-------

### Starting your server

Now that your handlers and server are all set up, you need to write a few more lines to tell asyncio to turn your
server on.

First, make sure the event loop will run your server. This is performed by 
telling it to create a [Task](https://docs.python.org/3/library/asyncio-task.html#asyncio.Task) which will be
automatically ran when the server starts up.

    if __name__ == "__main__":
        loop.create_task(main())
        
Next, you want to run the loop. However, if you want to kill the server, everything will error.  
In order to prevent this, you wrap the loop startup in a try/except block, catching KeyboardInterrupt:

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        my_handler.stop()
        loop.stop()

### Final Code

Here's the final code for the echo server:

    import asyncio
    import bfnet
    
    loop = asyncio.get_event_loop()
    
    my_handler = bfnet.get_handler(loop)
    
    @asyncio.coroutine
    def main():
        my_server = yield from my_handler.create_server(
        ("127.0.0.1", 8001), ("my_server.crt", "my_server.key", None))
        
        @my_server.any_data
        @asyncio.coroutine
        def echo(data, butterfly, handler):
            butterfly.write(data)
            
    if __name__ == "__main__":
        loop.create_task(main())
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            my_handler.stop()
            loop.stop()
        
Run this code, and open up an SSL client (`openssl s_client -connect localhost:8001`). Type in anything, and watch as
your message is bounced back to you.

------

Next, move onto the [Chat Server](/tutorial/chat_server) example.