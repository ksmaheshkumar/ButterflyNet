import asyncio
import logging

import Butterfly


logging.basicConfig(filename='/dev/null', level=logging.INFO)

formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(name)s - %(message)s')
root = logging.getLogger()

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
root.addHandler(consoleHandler)

from bfnet.BFHandler import ButterflyHandler


# Create your event loop.
loop = asyncio.get_event_loop()

class MyHandler(ButterflyHandler):
    def on_connection(self, butterfly: Butterfly):
        super().on_connection(butterfly)
        butterfly.flip_should_handle()


@asyncio.coroutine
def default_handler(self, butterfly: Butterfly, data: bytes):
    butterfly.write(data)


@asyncio.coroutine
def main():
    my_handler = MyHandler.get_handler(loop, log_level=logging.DEBUG, buffer_size=4096)
    my_server = yield from my_handler.create_server(("127.0.0.1", 8001), ("localhost.crt", "server.key", None))
    my_server.set_default_data_handler(default_handler)


if __name__ == '__main__':
    asyncio.ensure_future(main())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        exit(0)
