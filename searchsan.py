import argparse
import json
import concurrent.futures
import sys
import os
import http.client
import yaml

from urllib.parse import urlparse
from concurrent import futures

def savetofile(filename, data):
    with open(filename, 'a') as file:
        file.write(f'{data}\n')

def extract_hostname(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname

def extract_data(data):
    organic_results = data.get("organic", [])
    listdom = [result['link'] for result in organic_results]
    unique_domains = list(set(filter(None, listdom)))
    return unique_domains

def searcher(query, maxpage, country, language, perpage):
    try:
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({
            "q": query,
            "gl": country,
            "hl": language,
            "num": int(perpage),
            "page": int(maxpage)
        })
        headers = {
            'X-API-KEY': apidata['apikey'],
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        response = res.read().decode("utf-8")

        if "Unauthorized." in response:
            return "invalid-apikey"
        elif "Not enough credits" in response:
            return "not-enough-credits"
        elif "organic" not in response:
            return False
        else:
            datas = json.loads(response)
            result_domains = extract_data(datas)
            return result_domains

    except Exception as e:
        print(f"[ERROR] An unexpected error occurred in searcher: {str(e)}")
        return False
    finally:
        conn.close()

def gasken(query, args):
    try:
        if query in open(file_db_searched).read().splitlines():
            print(f"[INFO] This query ({query}) has been searched")
            return    

        for maxpage in range(1, int(args.maxpage)+1):
            results = searcher(query=query, maxpage=maxpage, country=args.country, language=args.language, perpage=args.perpage)
            if "invalid-apikey" == results:
                print(f"[SEARCH] Your apikey is invalid, recheck {file_config}")
                return
            elif "not-enough-credits" == results:
                print(f"[SEARCH] Not enough credits, recheck {file_config}")
                return
            elif not results:
                print(f"[SEARCH] Maxpage or result not found with query ({query}) in page {maxpage}")
                return

            if results:
                savetofile(file_db_searched, query)
                if args.exdomain:
                    ress_extractdomain = list(set(filter(None, [extract_hostname(result) for result in results])))
                    total = len(ress_extractdomain)
                    print(f"[SEARCH] Success get {total} unique domain with query ({query}) in page {maxpage}")
    
                    for text in ress_extractdomain:
                        if args.saveoutput:
                            savetofile(args.saveoutput, text)
                        if args.show:
                            print(f"[RESULTS] {text}")
                else:
                    total = len(results)
                    print(f"[SEARCH] Success get {total} unique urls with query ({query}) in page {maxpage}")

                    for text in results:
                        if args.saveoutput:
                            savetofile(args.saveoutput, text)
                        if args.show:
                            print(f"[RESULTS] {text}")
            else:
                print(f"[SEARCH] Failed with query ({query}) ")

    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {str(e)}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ql", "--query-list", dest="querylist", required=True, help="Input file with a list of query")
    parser.add_argument("-t", "--threads", dest="numthread", type=int, required=True, help="Number of threads")
    parser.add_argument("-o", "--output", dest="saveoutput", required=False, help="Output file to write found links")
    parser.add_argument("-exdom", "--extract-domain", dest="exdomain", required=False, action='store_true', help="Extract and filter unique domains")
    parser.add_argument("-maxpage", "--maxpage", dest="maxpage", required=False, help="Set the maximum page number (default: max of the page or 20 pages)", default="20")
    parser.add_argument("-perpage", "--perpage", dest="perpage", required=False, help="Set result urls per page (default: 100)", default="100")
    parser.add_argument("-country", "--country", dest="country", required=False, help="Set search by country (default: us)", default="us")
    parser.add_argument("-language", "--language", dest="language", required=False, help="Set search by language (default: en)", default="en")
    parser.add_argument("-show", "--show", dest="show", required=False, help="Print text results", action='store_true')
    return parser.parse_args()

if __name__ == "__main__":    
    header = """
                               __                   
    ________  ____ ___________/ /_  _________ _____ 
   / ___/ _ \\/ __ `/ ___/ ___/ __ \\/ ___/ __ `/ __ \\
  (__  )  __/ /_/ / /  / /__/ / / (__  ) /_/ / / / /
 /____/\\___/\\__,_/_/   \\___/_/ /_/____/\\__,_/_/ /_/     v.1.0-beta

          github.com/putunebandi
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(header)

    file_db_searched = "data/query_searched.txt"
    file_config = "configuration.yaml"
    try: 
        os.makedirs(os.path.dirname(file_db_searched), exist_ok=True)
        open(file_db_searched, 'a').close()
        with open(file_config, 'r') as file:
            apidata = yaml.safe_load(file)
        if not isinstance(apidata, dict) and 'apikey' in apidata:
            print(f"[INFO] Apikey not found in {file_config}")
            sys.exit(1)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    args = parse_args()
    try:
        numthread = args.numthread
        readsplit = open(args.querylist).read().splitlines()
        print(f"[INFO] Total query: {len(readsplit)}")
        print(f"[INFO] Started with {numthread} threads\n")
    except FileNotFoundError:
        print(f"File not found: {args.querylist}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

    with futures.ThreadPoolExecutor(max_workers=numthread) as executor:
        submitted_futures = {executor.submit(gasken, query, args): query for query in readsplit}
        
        try:
            for future in concurrent.futures.as_completed(submitted_futures):
                query = submitted_futures[future]
                future.result()
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Terminating all threads.")
            executor.shutdown(wait=False)
            sys.exit(1)
