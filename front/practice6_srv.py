import asyncio

import websockets


class SecureProxy:
    def __init__(self):
        self.control_drone = control_drone

    async def __call__(self, ws):
        async for msg in ws:
            if self.is_auth(ws):
                await self.control_drone(ws, ws.path, msg)
            else:
                ws.send("Access denied.")

    @staticmethod
    def is_auth(ws):
        print(ws.path)
        params = dict([ws.path.split("?")[1].split("=")])
        return params.get("token") == "valid_token"


async def control_drone(ws, path, msg):
    print(msg, path)
    if msg == "takeoff":
        print("Takeoff")
        await ws.send("takeoff receive")
    if msg == "land":
        await ws.send("land receive")
        print("Land")


async def main():
    proxy = SecureProxy()
    async with websockets.serve(proxy, "localhost", 8765) as srv:
        try:
            await srv.wait_closed()
        except Exception as e:
            print(e)
        # await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
