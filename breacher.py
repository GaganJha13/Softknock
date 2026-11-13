import argparse
import asyncio
import aiohttp

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=True)
parser.add_argument("-w", "--wordlist", required=True)
args = parser.parse_args()

c = "https://" + args.url.replace("https://", "").replace("http://", "").rstrip("/")

with open(args.wordlist) as f:
    a = [line.strip() for line in f if line.strip()]

async def fetch(session, url):
    try:
        async with session.get(url, allow_redirects=False) as response:
            if response.status in (200, 302, 401, 403):
                print(f'  \033[1;32m[+]\033[0m [{response.status}] {url}')
    except:
        pass

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in a:
            url = f"{c}/{i.lstrip('/')}"
            tasks.append(fetch(session, url))
        await asyncio.gather(*tasks)

asyncio.run(main())
print("\033[1;32m[+]\033[0m"*4 + "  Process Completed  " + "\033[1;32m[+]\033[0m"*4)