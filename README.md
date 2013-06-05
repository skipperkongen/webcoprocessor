# The Web Co-processor

## What is the basic idea?

1. A person opens a webpage in his browser
2. The webpage has a small javascript code that connects the browser (two-way connection) to a websocket on the server
3. The persons browser is now a *core* in the web co-processor. It can execute javascript on behalf of the server, and store transient data.

## Demo

The is a small demo of the web co-processor idea in the [code](./code) directory. To try the demo, do the following:

```bash
cd code
python server.py
# this starts the coordination server
```

Open the location [localhost:8888/demo](http://localhost:8888/demo) in a few browser tabs. Click the 'run query' button, and see how the tasks gets distributed to all the browsers (that *eval* some Javascript and send the result back to the browser tab that started the query).

