# Lab 02 - Ryan McClue (z5346008)

> TODO(Ryan): Technically packet time should not be get_ms() rather epoch_ms()

IMPORTANT(Ryan): INCLUDE SCREENSHOTS TO CONFIRM
# 1. Wireshark HTTP GET Request/Response
1. *What is the status code and phrase returned from the server to the client browser?*
Status Code: 200 
Status Phrase: OK 

2. *When was the HTML file that the browser is retrieving last modified at the server?*
`Tue, 23 Sep 2003, 5:29:00 GMT`
*Does the response also contain a DATE header?*
Yes. It's `Tue, 23 Sep 2003, 5:29:50 GMT`
*How are these two fields different?*
The Date header is the time when the server sent the response message.
The Last-Modified header is the time when the server believes the resource requested was last changed.

3. *Is the connection established between the browser and the server persistent or non-persistent?*
Persistent.
*How can you infer this?*
The presence of the header field `Connection: keep-alive` in the HTTP request/response
indicates that a single TCP connection can be used for multiple requests/responses.
Furthermore, using HTTP1.1

4. *How many bytes of content are being returned to the browser?*
73
(content-length or entire HTTP response?)

5. *What is the data contained inside the HTTP response packet?*
A html file containing: 
```
<html>
Congratulations.  You've downloaded the file lab2-1.html!
</html>
```

## 2. Wireshark HTTP Conditional GET Request/Response
1. *Inspect the contents of the first HTTP GET request from the browser to the server. Do you see an “IF-MODIFIED-SINCE” line in the HTTP GET?*
No

2. *Does the response indicate the last time that the requested file was modified?*
Yes. 

3. Now inspect the contents of the second HTTP GET request from the browser to the server. 
Do you see an “IF-MODIFIED-SINCE:” and “IF-NONE-MATCH” lines in the HTTP GET? 
If so, what information is contained in these header lines?


4. What is the HTTP status code and phrase returned from the server in response to this second HTTP GET? Did the server explicitly return the contents of the file? Explain.
304 Not Modified.

5. What is the value of the Etag field in the 2nd response message and how it is used? Has this value changed since the 1 st response message was received? 
ETage: "1bfef-173-8f4ae900"
