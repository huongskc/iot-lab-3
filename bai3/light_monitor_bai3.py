import asyncio
from datetime import datetime
import json
import aiocoap

URI = "coap://127.0.0.1:5683/iot/lab/light01/status"


async def main():
    protocol = await aiocoap.Context.create_client_context()
    print("Light Monitoring Client (CoAP Observe)")
    print(f"Connecting to: {URI}")
    print("Registering CoAP Observe...")

    request = aiocoap.Message(code=aiocoap.GET, uri=URI)
    request.opt.observe = 0

    requester = protocol.request(request)

    try:
        # 1. Nhan phan hoi trang thai ban dau
        initial_response = await requester.response
        now_str = datetime.now().strftime("%H:%M:%S")

        print("Observe registration successful")
        data = json.loads(initial_response.payload.decode("utf-8"))
        print(f"[{now_str}] Initial State")
        print(f"Device: {data.get('device_id', 'Unknown')}")
        print(f"Status: {data.get('status', 'Unknown')}")
        print("-" * 35)

        # 2. Tu dong nhan thong bao day tu Server khi trang thai thay doi (Khong dung loop GET)
        async for updated_response in requester.observation:
            now_str = datetime.now().strftime("%H:%M:%S")
            data = json.loads(updated_response.payload.decode("utf-8"))
            print(f"[{now_str}] State Updated")
            print(f"Device: {data.get('device_id', 'Unknown')}")
            print(f"Status: {data.get('status', 'Unknown')}")
            print("-" * 35)

    except (asyncio.CancelledError, KeyboardInterrupt):
        print("\nDa dung giam sat Observe.")
    finally:
        requester.observation.cancel()
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
