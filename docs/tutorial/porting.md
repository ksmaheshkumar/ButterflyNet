# Porting Synchronous code to ButterflyNet

You want to use ButterflyNet for your next project/existing project, because you think it's amazing and great.  
However, you want to use a library that uses non-async code, which will block up your server for a long time
until it finishes.  

There's an easy solution to this.

## Running your code in an executor

Executors allow you to run your blocking code in a different thread to your main loop, effectively meaning you
don't block the event loop, allowing your code to continue running normally. asyncio and concurrent handles 
communication between the executors and your main thread, meaning you don't have to do anything other than
call the utility functions and get the results back.

Executors can be read about in more detail [here](https://docs.python.org/3/library/concurrent.futures.html).

Your ButterflyHandler has methods for running your code in a different executor, as well as a method for
setting which executor to run your code in.

-------

## Running in a Future

To run your code in an executor, you would call `ButterflyHandler.async_func(func)`.   
For example:

    @my_server.set_handler
    @asyncio.coroutine
    def handle_packets(butterfly: PacketButterfly):
        while True:
            packet = yield from butterfly.read()
            # Run your blocking code here
            fut = butterfly.handler.async_func(somelibrary.some_long_running_function)
    
    
`async_func` returns a new [Future](https://docs.python.org/3/library/asyncio-task.html#asyncio.Future) object
that you can check for the result of your function.

## Waiting for the Future

If you don't feel like checking the future yourself, you can instead call `ButterflyHandler.async_and_wait(func)`.

    @my_server.set_handler
    @asyncio.coroutine
    def handle_packets(butterfly: PacketButterfly):
        while True:
            packet = yield from butterfly.read()
            # Run your blocking code here
            # And get the result as soon as it's finished
            result = yield from butterfly.handler.async_and_wait(somelibrary.other_long_function)
            

## Changing the executor

If you need to bypass the GIL, you can change the Executor from a `ThreadPoolExecutor` to a `ProcessPoolExecutor` 
which uses the Multiprocessing module. Be aware of the usual woes with using multiprocessing instead of threading,
however.
<br>

    my_handler.set_executor(concurrent.futures.ProcessPoolExecutor())
    

    