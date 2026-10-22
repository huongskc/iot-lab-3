import asyncio
import json
import aiocoap
import aiocoap.resource as resource

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5683
DEVICE_ID = "light01"


class LightResource(resource.ObservableResource):
    """Tai nguyen den thong minh ho tro GET, PUT va Observe tai /iot/lab/light01/status."""

    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id
        self.status = "OFF"  # Trang thai mac dinh ban dau la OFF

    async def render_get(self, request):
        if request.opt.observe is not None:
            print("New Observe registration received")

        data = {
            "device_id": self.device_id,
            "status": self.status
        }
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=json.dumps(data).encode("utf-8"),
            content_format=50
        )

    async def render_put(self, request):
        try:
            body = json.loads(request.payload.decode("utf-8"))
            dev_id = body.get("device_id")
            command = str(body.get("command", "")).strip().upper()
        except Exception as e:
            print(f"[Loi] Parse PUT payload that bai: {e}")
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload=b"Payload JSON khong hop le"
            )

        print("\nPUT request received:")
        print(f"Device: {dev_id}")
        print(f"Command: {command}")

        if command in ["ON", "OFF"]:
            old_state = self.status
            if self.status != command:
                self.status = command
                print(f"Light state changed: {old_state} -> {self.status}")
                print(f"Notify observers: {self.status}")
                # Thong bao trang thai moi toi tat ca clients dang observe
                self.updated_state()
            else:
                print(f"Light state giu nguyen: {self.status}")

            return aiocoap.Message(
                code=aiocoap.CHANGED,
                payload=json.dumps({
                    "device_id": self.device_id,
                    "status": self.status
                }).encode("utf-8"),
                content_format=50
            )
        else:
            print(f"Lenh khong hop le: {command}")
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload=f"Lenh '{command}' khong hop le. Chi chap nhan ON hoac OFF.".encode("utf-8")
            )


async def main():
    root = resource.Site()
    light_res = LightResource(DEVICE_ID)
    root.add_resource(["iot", "lab", DEVICE_ID, "status"], light_res)

    server_context = await aiocoap.Context.create_server_context(
        root, bind=(SERVER_HOST, SERVER_PORT)
    )

    print("CoAP Smart Light Server started...")
    print(f"Resource: /iot/lab/{DEVICE_ID}/status")
    print(f"URI: coap://localhost:{SERVER_PORT}/iot/lab/{DEVICE_ID}/status")
    print("Nhan Ctrl+C de dung Server.\n")

    try:
        await asyncio.get_running_loop().create_future()
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass
    finally:
        print("\nDang tat Smart Light Server...")
        await server_context.shutdown()
        print("Smart Light Server da tat.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
