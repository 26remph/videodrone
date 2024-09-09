import asyncio

import websockets


async def control_drone(ws):
    async for msg in ws:
        print(msg)
        if msg == "takeoff":
            print("Takeoff")
            await ws.send("takeoff receive")
        if msg == "land":
            await ws.send("land receive")
            print("Land")


async def main():
    async with websockets.serve(control_drone, "localhost", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
