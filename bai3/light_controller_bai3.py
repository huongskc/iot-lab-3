import asyncio
import json
import aiocoap

URI = "coap://127.0.0.1:5683/iot/lab/light01/status"
DEVICE_ID = "light01"


async def main():
    protocol = await aiocoap.Context.create_client_context()
    print("Light Controller Client started...")
    print(f"Ket noi toi: {URI}")
    print("Huong dan:")
    print("- ON: Bat den")
    print("- OFF: Tat den")
    print("- STATUS: Xem trang thai hien tai (GET)")
    print("- EXIT: Thoat chuong trinh")
    print("=" * 40)

    try:
        while True:
            # Nhap lenh tu ban phim khong block event loop
            raw_input = await asyncio.to_thread(input, "Nhap lenh (ON/OFF/STATUS/EXIT): ")
            cmd = raw_input.strip().upper()

            if not cmd:
                continue

            if cmd == "EXIT":
                print("Dang thoat Controller Client...")
                break

            elif cmd == "STATUS":
                print("Sending GET request...")
                try:
                    request = aiocoap.Message(code=aiocoap.GET, uri=URI)
                    response = await protocol.request(request).response
                    print("Response:")
                    print(response.payload.decode("utf-8"))
                except Exception as e:
                    print(f"[Loi] Khong the gui GET: {e}")

            elif cmd in ["ON", "OFF"]:
                print("Sending PUT request...")
                put_payload = json.dumps({
                    "device_id": DEVICE_ID,
                    "command": cmd
                }).encode("utf-8")

                try:
                    request = aiocoap.Message(
                        code=aiocoap.PUT,
                        uri=URI,
                        payload=put_payload,
                        content_format=50
                    )
                    response = await protocol.request(request).response
                    print(f"Response Code: {response.code}")
                    if cmd == "ON":
                        print(f"Da bat den {DEVICE_ID}")
                    else:
                        print(f"Da tat den {DEVICE_ID}")
                except Exception as e:
                    print(f"[Loi] Khong the gui PUT: {e}")

            else:
                print(f"[Loi] Lenh '{cmd}' khong hop le! Chi chap nhan ON, OFF, STATUS, EXIT.")

    except (asyncio.CancelledError, KeyboardInterrupt):
        print("\nDa dung Controller.")
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
