import argparse
import asyncio
import logging
import pyhy

from libottdadmin2.client.asyncio import OttdAdminProtocol
from libottdadmin2.constants import NETWORK_ADMIN_PORT

parser = argparse.ArgumentParser(description='Connect to OpenTTD via asyncio')
parser.add_argument('--password', default='123qwe', help="The password to connect with")
parser.add_argument('--host', default='127.0.0.1', help="The host to connect to")
parser.add_argument('--port', default=NETWORK_ADMIN_PORT, type=int, help="The port to connect to")

args = parser.parse_args()

master_key = b'\xb8\x1f\xb6\x86\x04\xd9"\x14\xcf\xdbe\xea1+\xee\xc8\x0c\x87\xd4\xde7\x8c:k&\xb5\xe6C\x02\x01s\xd6'
deriv_key = pyhy.hydro_pwhash_deterministic(args.password, "ADM_PORT", master_key)
keypair = pyhy.hydro_sign_keygen_deterministic(deriv_key)

print("our pubkey: " + bytearray(keypair.pk).hex())

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    client = loop.run_until_complete(OttdAdminProtocol.connect(loop=loop, host=args.host, port=args.port,
                                                               keypair=keypair))
    loop.run_until_complete(client.client_active)
