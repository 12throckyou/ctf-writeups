# Baby Web

Challenge Description:
What's going on with this website?! Weird characters keep popping up.

No need to bruteforce
http://34.76.206.46:10008 

The URL redirects to http://34.76.206.46:10008/?page=0

It appears to be a random character everytime the page is visted

After a bit more testing "page" 1, 2 and 3 always gave the same letter.

So i wrote a script to see when the same letter is showing up.

```
def doreq(page):
    params = {
        'page': page,
    }
    r = requests.get('http://34.76.206.46:10008/', params=params)
    output = f"page: {page} has {r.text}"
    return output
    
i = 1
while i <= 100:
    req1 = doreq(i)
    req2 = doreq(i)
    if(req1 == req2):
        print(req1)
    i += 1
```

this output gave me the first few pages that would always repeat the same character 

```
page: 1 has m
page: 2 has 4
page: 3 has k
page: 5 has i
page: 8 has n
page: 13 has g
page: 21 has _
```

I tried to brute force the first 1000 pages but was only getting part of the flag or response. That is when I saw the numbers were the fibonacci sequence.

Adding this into my script and running it now:

```
import requests
import time

def doreq(page):
    params = {
        'page': page,
    }
    r = requests.get('http://34.76.206.46:10008/', params=params)
    output = f"page: {page} has {r.text}"
    return r.text

fib = [1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597,2584,4181,6765,10946,17711,28657,46368,75025,121393,196418,317811,514229,832040,1346269,2178309,3524578,5702887,9227465,14930352,24157817,39088169,63245986,102334155,165580141,267914296,433494437,701408733,1134903170,1836311903,2971215073,4807526976,7778742049,12586269025,20365011074,32951280099,53316291173,86267571272,139583862445,225851433717,365435296162,591286729879,956722026041,1548008755920,2504730781961,4052739537881,6557470319842,10610209857723,17167680177565]


i = 0
while i <= 63:
    x = fib[i]
    req1 = doreq(x)
    print(req1,end='')
    time.sleep(0.2)
    i += 1
```

m4king_1t_b1g_s0_th4t_y0u_h4ve_t0_scr1pt_jadeCTF{f1bonacci_FTW!}

flag: jadeCTF{f1bonacci_FTW!}





    
