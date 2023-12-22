# publish_to_nostr.py
# author: TJ Murphy
# Date: 11/18/2023
# Purpose: This script publishes an event to Nostr.
# this is working without errors, but not yet used in the pipeline

import nostr
import ssl
import time
from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.delegation import Delegation
from nostr.event import EventKind, Event
from nostr.key import PrivateKey

def publish_event_to_nostr(message):
    # Generate a key pair
    private_key = PrivateKey()
    public_key = private_key.public_key
    print(f"Private key: {private_key.bech32()}")
    print(f"Public key: {public_key.bech32()}")

    # Relay manager setup
    relay_manager = RelayManager()
    relay_manager.add_relay("wss://nostr-pub.wellorder.net")  # Example relay
    relay_manager.add_relay("wss://relay.damus.io")  # Another example relay
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE})
    time.sleep(1.25)  # Allow connections to open

    # Create and sign an event
    event = Event(public_key.hex(), message)
    private_key.sign_event(event)

    # Publish the event
    relay_manager.publish_event(event)
    time.sleep(1)  # Allow the message to send

    # Close connections
    relay_manager.close_connections()


# Example usage
publish_event_to_nostr("Hello Nostr from Python script!")
