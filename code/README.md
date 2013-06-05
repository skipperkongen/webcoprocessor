# Try the demo

The is a small demo of the web co-processor idea in the [code](./code) directory. To try the demo, do the following:

```bash
cd code # this directory
python server.py
# this starts the coordination server
```

Open the location [localhost:8888/demo](http://localhost:8888/demo) in a few browser tabs. Click the 'run query' button, and see how the tasks gets distributed to all the browsers (that *eval* some Javascript and send the result back to the browser tab that started the query).
