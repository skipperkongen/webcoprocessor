# When the server asks the client to compute stuff

The idea is that when a client asks a server to perform service *A*, the server asks the client back to perform service *B*.

I call the concept *client-queries* to indicate that it is the server asking the client for a service. The query *piggy-back rides* inside the result returned by service *A*:

Example:

```
request: http://server/getstuff
response: {
	"result": 42, 
	"client-query": "find value such that md5(value) = 00004328478239", 
	"response-url": "http://server/answer?value={x}"
	}
```

Which means: "Here is the stuff you asked for (the number 42). Would you be so kind and solve this other problem for me in return, and let me know the answer by calling this URL?"

Additional thought:

* What kinds of queries clients can solve using Javascript? 
* What are the essential tasks that aid scalability in a given domain?
* Should there be a reward system, where clients get points for performing service *B* which go towards discounts for service A?