import asyncio
from datetime import datetime
import json
import aiocoap

URI = "coap://127.0.0.1:5683/iot/lab/sensor01/data"
POLL_INTERVAL = 3  # giay


async def main():
    protocol = await aiocoap.Context.create_client_context()
    print("Monitoring CoAP Client started...")
    print(f"Dang giam sat: {URI}")
    print("Truy van dinh ky moi 3s. Nhan Ctrl+C de dung.\n")

    try:
        while True:
            try:
                request = aiocoap.Message(code=aiocoap.GET, uri=URI)
                response = await protocol.request(request).response
                now_str = datetime.now().strftime("%H:%M:%S")

                data = json.loads(response.payload.decode("utf-8"))
                device = data.get("device_id", "Unknown")
                temp = data.get("temperature", 0.0)
                humi = data.get("humidity", 0.0)

                print(f"[{now_str}] Received sensor data")
                print(f"Device: {device}")
                print(f"Temperature: {temp} C")
                print(f"Humidity: {humi} %")

                has_alert = False
                if temp > 35:
                    print("CANH BAO: Nhiet do cao")
                    has_alert = True
                if humi < 40:
                    print("CANH BAO: Do am thap")
                    has_alert = True
                if not has_alert:
                    print("Trang thai: Binh thuong")

                print("-" * 35)

            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] [Loi truy van]: {e}")

            await asyncio.sleep(POLL_INTERVAL)

    except (asyncio.CancelledError, KeyboardInterrupt):
        print("\nDa dung giam sat.")
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
