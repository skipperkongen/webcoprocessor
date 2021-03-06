# The Web Co-processor*

## What is the basic idea?

1. A person opens a webpage in his browser
2. The webpage has a small javascript code that opens a two-way connection between the browser and server via a websocket
3. The persons browser is now a *core* in the web co-processor. A "core" = transient CPU ([executes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval) Javascript) and storage ([Web Storage](http://en.wikipedia.org/wiki/Web_storage)).
4. A core can execute javascript on behalf of other web cores (or the server), and store transient data.

If you are thinking *botnet*, you are forgiven. The idea is similar, but the intent different.

<img src="https://docs.google.com/drawings/d/1rBgKMcpj4UwuuJfBXKrpSWS0QkbhT2eZXmXOJtrkG8E/pub?w=749&amp;h=483">

## Demo

The is a small demo of the web co-processor idea in the [code](./code) directory. To try the demo, do the following:

```bash
cd code
python server.py
# this starts the coordination server
```

Open the location [localhost:8888/demo](http://localhost:8888/demo) in a few browser tabs. Click the 'run query' button, and see how the tasks gets distributed to all the browsers (that *eval* some Javascript and send the result back to the browser tab that started the query).

*) Credit for name Web Co-Processor goes to Marcos Vaz Salles. Idea behind Web Co-Processor is due to Pimin Konstantin Kefaloukos.

