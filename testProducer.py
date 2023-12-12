import requests
import asyncio
async def api_1(number):
    res = requests.get(f'https://jsonplaceholder.typicode.com/posts/{number}')
    return res.json()

async def api_2(number):
    res = requests.get(f'https://jsonplaceholder.typicode.com/comments/{number}')
    return res.json()

async def main(number):
    task1 = asyncio.create_task(api_1(number))
    task2 = asyncio.create_task(api_2(number))
    result_of_task1 = await task1
    result_of_task2 = await task2
    return result_of_task1, result_of_task2
