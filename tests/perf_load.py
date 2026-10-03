"""Simple concurrency smoke-test helper for FitBuddy.
Run the server in mock-AI mode first, then execute this script.
"""
import concurrent.futures, time, httpx
URL="http://127.0.0.1:8000/health"
def one(_):
    t=time.perf_counter(); r=httpx.get(URL,timeout=10); return time.perf_counter()-t,r.status_code
if __name__=="__main__":
    for n in (1,10,25):
        with concurrent.futures.ThreadPoolExecutor(max_workers=n) as ex:
            vals=list(ex.map(one,range(n)))
        print(n,"users", "errors=",sum(s!=200 for _,s in vals),"avg_s=",sum(t for t,_ in vals)/len(vals))
