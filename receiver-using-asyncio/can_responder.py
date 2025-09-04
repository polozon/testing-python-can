
import asyncio
from typing import TYPE_CHECKING

import can

if TYPE_CHECKING:
    from can.notifier import MessageRecipient

async def main() -> None:
    """
    Listens for CAN messages on vcan0 and responds to messages with ID 10.
    """
    with can.Bus(
        interface="socketcan", channel="vcan0", receive_own_messages=False
    ) as bus:
        reader = can.AsyncBufferedReader()

        # Reading don't work without this
        listeners: list[MessageRecipient] = [
            reader,  # AsyncBufferedReader() listener
        ]

        # Create Notifier and assign it to a variable
        notifier = can.Notifier(bus, listeners, loop=asyncio.get_running_loop())

        for _ in range(10):
            print("Listening for CAN messages on vcan0... And specially for ID 10")
            msg = await reader.get_message()
            print(f"Received message with arbitration id = {msg.arbitration_id}")
            if msg.arbitration_id == 10:
                print(f"YES! The id is 10, Sending DEADBEEF back at you!")
                response_msg = can.Message(
                    arbitration_id=11,
                    data=[0xDE, 0xAD, 0xBE, 0xEF],
                    is_extended_id=False
                )
                try:
                    bus.send(response_msg)
                    print(f"Sent message: {response_msg}")
                except can.CanError:
                    print("Failed to send message")
        print("Shutting down...")
        notifier.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped by user")
