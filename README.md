# The Web Co-processor

The idea is the following. Every person viewing a webpage (containing a small piece of javascript code) becomes a core in the web co-processor. If 1000 people are viewing the page, there are 1000 cores. The technology is based on websockets between the client and server, and a server side code that parallelizes a tasks received from one core, and send the subtasks to all the other cores.

The idea is that any of the connected people can use the combined computing power of all the other people who are connected to collectively solve some problem. Good tasks are computationally expensive, but only need small amounts of data, and the ability to prove answers correct. The archetypical task is bruteforcing cryptographic hashes.

