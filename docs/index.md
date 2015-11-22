#### ![ButterflyNet - Drawn by Tudor Iacobescu](/bnet.png)

ButterflyNet is a server-side batteries-included secure networking framework built upon [asyncio](https://docs.python.org/3/library/asyncio.html). 

All code in ButterflyNet is designed to be asynchronous by default, with special cases made for non-async code such as external libraries.  
Because of the heavy usage of asyncio, this module does not officially support Python versions before 3.4. It may be possible to run it with a backported tulip library, but no official support will be given for this.

### Why ButterflyNet?

ButterflyNet was designed for a few main reasons:
  
  - Sockets are low-level; personally, I dislike them because they're not the friendliest thing to use.
  - Twisted is a clusterfuck.
  - asyncio networking is good, but it's very hands-off - ButterflyNet comes with everything needed for a full networking suite.
  
All the existing libraries are not, by design, secure. You can work around this with SSLContexts - however, ButterflyNet forces TLS with secure settings on your server by default.

### Getting Started

If you're new to asyncio, it's recommended you read the [documentation](https://docs.python.org/3/library/asyncio.html) on it before beginning to use ButterflyNet. It is heavily based upon the event loop in asyncio, and as such you need an understanding of how it works.   
If you're new to ButterflyNet, see the [Tutorial](/tutorial/starting/).  
If you're porting non-async code to ButterflyNet or using it to create a network accessible app, see the [Porting Guide](/tutorial/porting/).
  
### Limitations

You have a choice of TCP or UDP in most networking frameworks. However, ButterflyNet is designed upon persistent, TLS-authenticated and secured connections, of which UDP has:

 - No persistent connections
 - Unreliable TLS security
 
This means ButterflyNet is locked to TCP for the future. OpenSSL *does* support DTLS, but no support for this is planned.




