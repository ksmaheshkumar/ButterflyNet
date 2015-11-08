## ButterflyNet

### What is ButterflyNet?

ButterflyNet is an server-side batteries-included secure networking framework built upon [asyncio](https://docs.python.org/3/library/asyncio.html).  
All code in ButterflyNet is designed to be asynchronous by default, with special cases made for non-async code such as external libraries.  
Because of the heavy usage of asyncio, this module does not officially support Python versions before 3.4. It may be possible to run it with a backported tulip library, but no official support will be given for this.

### Why ButterflyNet?

ButterflyNet was designed for a few main reasons:
  
  - Sockets are low-level; personally, I dislike them because they're not the friendliest thing to use.
  - Twisted is a clusterfuck.
  - asyncio networking is good, but it's very hands-off - ButterflyNet comes with everything needed for a full networking suite.
  
All the existing libraries are not, by design, secure. You can work around this with SSLContexts - however, ButterflyNet forces TLS with secure settings on your server by default.
  
### Getting started

Tutorials and getting started guides can be found at the [docs](https://butterflynet.veriny.tf/).

You can also see examples [here](https://github.com/SunDwarf/ButterflyNet/tree/master/examples).