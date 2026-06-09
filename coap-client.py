import sys
import asyncio
import aiocoap
import aiocoap.numbers.constants as cc
from aiocoap.oscore import FilesystemSecurityContext

async def send_rest_request(method_verb, payload_str=None):
	# 1. Network tuning
	cc.TransportTuning.ACK_TIMEOUT = 25.0
	cc.TransportTuning.MAX_RETRANSMIT = 2

	# 2. Client and OSCORE setup
	client = await aiocoap.Context.create_client_context()
	oscore_ctx = FilesystemSecurityContext("security/my_zone")
	client.client_credentials["coap://localhost/test"] = oscore_ctx

	# 3. Choose the payload bytes
	payload_bytes = payload_str.encode() if payload_str else b""

	# 4. Craft and send the specific REST method
	req = aiocoap.Message(
		code=method_verb,
		uri=sys.argv[1], # EXAMPLE coap://localhost/test
		payload=payload_bytes
	)

	try:
		res = await client.request(req).response
		print(f"[{method_verb.name}] Response Code: {res.code} | Payload: {res.payload.decode()}")
	except Exception as e:
		print(f"Error: {e}")
	finally:
		await client.shutdown()

async def main():
	# METHOD CHECK
	if sys.argv[2] == "GET":
		await send_rest_request(aiocoap.GET)
	elif sys.argv[2] == "POST":
		await send_rest_request(aiocoap.POST, sys.argv[3]) #'{"item": "sensor_1", "status": "active"}')
	elif sys.argv[2] == "PUT":
		await send_rest_request(aiocoap.PUT, sys.argv[3]) #'{"status": "inactive"}')
	elif sys.argv[2] == "DELETE":
		await send_rest_request(aiocoap.DELETE)

if __name__ == "__main__":
	asyncio.run(main())

