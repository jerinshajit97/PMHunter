import requests
import json
import logging
import tldextract
import sys
import textwrap
import argparse

# argument parser
# description
parser = argparse.ArgumentParser(usage='%(prog)s -h for help',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
        ░░░░░░░▄█▄▄▄█▄
▄▀░░░░▄▌─▄─▄─▐▄░░░░▀▄
█▄▄█░░▀▌─▀─▀─▐▀░░█▄▄█
░▐▌░░░░▀▀███▀▀░░░░▐▌   █▀█ █▀▄▀█ █░█ █░█ █▄░█ ▀█▀ █▀▀ █▀█
████░▄█████████▄░████  █▀▀ █░▀░█ █▀█ █▄█ █░▀█ ░█░ ██▄ █▀▄ Version 1.1
        '''))
parser.add_argument('-f', help='file name') #adding arguments
args = parser.parse_args()
#print(args)
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = False

def findCount(val): #funtion to find total count
    wurl='https://bifrost-web-https-v4.gw.postman.com/ws/proxy'
    qh = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0","Content-Type":"application/json"}

    #workspace  
    dw = {"service":"search","method":"POST","path":"/search","body":{"queryIndex":"collaboration.workspace","queryText":val,"from":0,"size":1}}
    #team
    dt = {"service":"search","method":"POST","path":"/search","body":{"queryIndex":"apinetwork.team","queryText":val,"from":0,"size":1}}
    #collection
    dc = {"service":"search","method":"POST","path":"/search","body":{"queryIndex":"runtime.collection","queryText":val,"from":0,"size":1}}
    #api
    da = {"service":"search","method":"POST","path":"/search","body":{"queryIndex":"adp.api","queryText":val,"from":0,"size":1}}

    jdw = json.dumps(dw)
    jdt = json.dumps(dt)
    jdc = json.dumps(dc)
    jda = json.dumps(da)

    rw = requests.post(url = wurl, headers = qh, data = jdw)
    rt = requests.post(url = wurl, headers = qh, data = jdt)
    rc = requests.post(url = wurl, headers = qh, data = jdc)
    ra = requests.post(url = wurl, headers = qh, data = jda)

    # print(r.text)
    WTotal = json.loads(rw.text)["meta"]["total"] # geting total no of workspace
    TTotal = json.loads(rt.text)["meta"]["total"] # geting total no of team
    CTotal = json.loads(rc.text)["meta"]["total"] # geting total no of collection
    ATotal = json.loads(ra.text)["meta"]["total"] # geting total no of api
    
   # print("workspace:%s \nteam:%s \ncollection:%s \napi:%s"%(WTotal,TTotal,CTotal,ATotal))

    result = {"W":WTotal,"T":TTotal,"C":CTotal,"A":ATotal}

    return result


def SwaggerCount(val):
    surl='https://app.swaggerhub.com/apiproxy/specs?sort=BEST_MATCH&order=DESC&query='+val+'&limit=0'
    qh = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"}
    sr = requests.get(url = surl, headers = qh)
    count=json.loads(sr.text)["totalCount"]
    return count

#print logo
print(r"""░░░░░░░▄█▄▄▄█▄
▄▀░░░░▄▌─▄─▄─▐▄░░░░▀▄
█▄▄█░░▀▌─▀─▀─▐▀░░█▄▄█
░▐▌░░░░▀▀███▀▀░░░░▐▌   █▀█ █▀▄▀█ █░█ █░█ █▄░█ ▀█▀ █▀▀ █▀█
████░▄█████████▄░████  █▀▀ █░▀░█ █▀█ █▄█ █░▀█ ░█░ ██▄ █▀▄ Version 1.1""")

# function to display output
def display(val):
    out="[ Workspace:"+str(val["W"])+" | Team:"+str(val["T"])+" | Collection:"+str(val["C"])+" | Api:"+str(val["A"])+" ]"
    return out

f = open(args.f, "r").read().splitlines()
#print(f.readlines())

pre='' # vriable to store dmain to execute it only once
for x in f:
    if tldextract.extract(x).domain != pre and tldextract.extract(x).suffix != '':
        
        fin = tldextract.extract(x).domain 
        fin1 = tldextract.extract(x).domain+'.'+tldextract.extract(x).suffix

        print("%s ::POSTMAN:: %s [ https://www.postman.com/search?q=%s&scope=all&type=all ]"%( fin, display(findCount(fin)), fin ))
        print("%s ::SWAGGER:: %s [ https://app.swaggerhub.com/search?query=%s&sort=BEST_MATCH&order=DESC ]"%(fin, SwaggerCount(fin), fin))
       
        print("%s ::POSTMAN:: %s [ https://www.postman.com/search?q=%s&scope=all&type=all ]"%(fin1, display(findCount(fin1)), fin1 ))
        print("%s ::SWAGGER:: %s [ https://app.swaggerhub.com/search?query=%s&sort=BEST_MATCH&order=DESC ]"%(fin1, SwaggerCount(fin1), fin1 ))
        pre=tldextract.extract(x).domain
       # if fin1 != x: # for testing first domain
       #     print("%s :::: %s\n"%(x, display(findCount(x) ) ) ) 
    else:
        if tldextract.extract(x).subdomain != 'www':
            print("%s ::POSTMAN:: %s [ https://www.postman.com/search?q=%s&scope=all&type=all ]"%(x, display(findCount(x)), x ))
            print("%s ::SWAGGER:: %s [ https://app.swaggerhub.com/search?query=%s&sort=BEST_MATCH&order=DESC ]\n"%(x, SwaggerCount(x), x ))


