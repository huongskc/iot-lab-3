import asyncio
import json
import random
from datetime import datetime
import aiocoap
import aiocoap.resource as resource

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5683
DEVICE_ID = "sensor01"
UPDATE_INTERVAL = 3  # giay


class SensorResource(resource.Resource):
    """Tai nguyen cung cap du lieu cam bien tai URI /iot/lab/sensor01/data."""

    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id
        self.temperature = 28.5
        self.humidity = 65.2

    def update_sensor_values(self):
        # Sinh ngau nhien nhiet do (20.0 - 40.0) va do am (30.0 - 80.0)
        self.temperature = round(random.uniform(20.0, 40.0), 1)
        self.humidity = round(random.uniform(30.0, 80.0), 1)

    async def render_get(self, request):
        data = {
            "device_id": self.device_id,
            "temperature": self.temperature,
            "humidity": self.humidity
        }
        payload = json.dumps(data).encode("utf-8")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] GET request handled -> {data}")

        # Tra ve JSON voi content_format la application/json (ma 50)
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=payload,
            content_format=50  # 50 = application/json
        )


async def sensor_updater_task(sensor_res):
    """Cap nhat chi so cam bien moi 3 giay."""
    while True:
        await asyncio.sleep(UPDATE_INTERVAL)
        sensor_res.update_sensor_values()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [Cap nhat cam bien] Nhiet do: {sensor_res.temperature}°C, Do am: {sensor_res.humidity}%")


async def main():
    root = resource.Site()
    sensor_res = SensorResource(DEVICE_ID)
    root.add_resource(["iot", "lab", DEVICE_ID, "data"], sensor_res)

    server_context = await aiocoap.Context.create_server_context(
        root, bind=(SERVER_HOST, SERVER_PORT)
    )

    print("Sensor CoAP Server started...")
    print(f"Resource available: coap://localhost:{SERVER_PORT}/iot/lab/{DEVICE_ID}/data")
    print(f"Cap nhat du lieu cam bien moi {UPDATE_INTERVAL}s. Nhan Ctrl+C de dung.\n")

    updater = asyncio.create_task(sensor_updater_task(sensor_res))

    try:
        await asyncio.get_running_loop().create_future()
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass
    finally:
        updater.cancel()
        print("\nDang tat Sensor Server...")
        await server_context.shutdown()
        print("Sensor Server da tat.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
