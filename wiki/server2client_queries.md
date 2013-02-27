# When the server asks the client to compute stuff

The idea is that a server which provides service *A*, asks clients to provide service *B* in return. I call the concept *client-queries*, and I think it is brilliant.
If this idea could be leveraged towards scalable systems, that would be cool.

Example:

```
request: http://server/getstuff
response: {
	"result": 43, 
	"client-query": "find value such that md5(value) = 00004328478239", 
	"response-url": "http://server/answer?value={x}"
	}
```