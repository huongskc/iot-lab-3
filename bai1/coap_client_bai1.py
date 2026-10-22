import asyncio
import aiocoap

URI = "coap://127.0.0.1:5683/iot/lab/message"
STUDENT_ID = "B23DCCN378"
STUDENT_NAME = "Nguyen Van Huong"
POST_PAYLOAD = f"Xin chao tu CoAP Client - {STUDENT_ID} - {STUDENT_NAME}"


async def main():
    protocol = await aiocoap.Context.create_client_context()

    print("CoAP Client")
    print("=" * 40)

    # 1. Thuc hien yeu cau GET
    print("Sending GET request...")
    print(f"URI: {URI}")
    try:
        get_request = aiocoap.Message(code=aiocoap.GET, uri=URI)
        get_response = await protocol.request(get_request).response
        print("Response:")
        print(f"Code: {get_response.code}")
        print(f"Payload: {get_response.payload.decode('utf-8')}")
    except Exception as e:
        print(f"[Loi] Khong the gui GET: {e}")

    print("-" * 40)

    # 2. Thuc hien yeu cau POST
    print("Sending POST request...")
    print(f"Payload: {POST_PAYLOAD}")
    try:
        post_request = aiocoap.Message(
            code=aiocoap.POST,
            uri=URI,
            payload=POST_PAYLOAD.encode("utf-8")
        )
        post_response = await protocol.request(post_request).response
        print("Response:")
        print(f"Code: {post_response.code}")
        print(f"Payload: {post_response.payload.decode('utf-8')}")
    except Exception as e:
        print(f"[Loi] Khong the gui POST: {e}")

    await protocol.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
