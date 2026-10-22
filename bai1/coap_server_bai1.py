import asyncio
from datetime import datetime
import aiocoap
import aiocoap.resource as resource

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5683


class MessageResource(resource.Resource):
    """Tai nguyen xu ly GET va POST tai URI /iot/lab/message."""

    def __init__(self):
        super().__init__()
        self.last_message = "Xin chao tu CoAP Server"

    async def render_get(self, request):
        print(f"GET request received: /iot/lab/message")
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=self.last_message.encode("utf-8")
        )

    async def render_post(self, request):
        payload_str = request.payload.decode("utf-8")
        now_str = datetime.now().strftime("%H:%M:%S")

        print("POST request received:")
        print(f"Payload: {payload_str}")
        print(f"Time: {now_str}")
        print("-" * 40)

        # Luu lai thong diep POST gan nhat
        self.last_message = payload_str

        # Tra ve phan hoi 2.04 Changed
        return aiocoap.Message(
            code=aiocoap.CHANGED,
            payload="Server da nhan thong diep".encode("utf-8")
        )


async def main():
    root = resource.Site()
    root.add_resource(["iot", "lab", "message"], MessageResource())

    server_context = await aiocoap.Context.create_server_context(
        root, bind=(SERVER_HOST, SERVER_PORT)
    )
    print(f"CoAP Server started on port {SERVER_PORT}")
    print(f"Resource available: coap://localhost:{SERVER_PORT}/iot/lab/message")
    print("Nhan Ctrl+C de dung Server.\n")

    try:
        # Giu server chay vo han
        await asyncio.get_running_loop().create_future()
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass
    finally:
        print("\nDang tat CoAP Server...")
        await server_context.shutdown()
        print("CoAP Server da tat.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
