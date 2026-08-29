import asyncio
async def fetch(url):
    await asyncio.sleep(0.05)
    return 'ok'
async def _run(urls):
    return await asyncio.gather(*(fetch(u) for u in urls))
def main(urls):
    return asyncio.run(_run(urls))
