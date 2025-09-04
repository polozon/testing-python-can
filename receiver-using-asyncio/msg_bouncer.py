#!/usr/bin/env python

"""
This example demonstrates how to use async IO with python-can.
"""

import asyncio
from typing import TYPE_CHECKING

import can

if TYPE_CHECKING:
    from can.notifier import MessageRecipient


def print_message(msg: can.Message) -> None:
    """Regular callback function. Can also be a coroutine."""
    print(msg)

async def main() -> None:
    """The main function that runs in the loop."""

    with can.Bus(
        interface="socketcan", channel="vcan0", receive_own_messages=True
    ) as bus:
        reader = can.AsyncBufferedReader()
        logger = can.Logger("logfile.asc")

        listeners: list[MessageRecipient] = [
            print_message,  # Callback function
            reader,  # AsyncBufferedReader() listener
            logger,  # Regular Listener object
        ]

        print("Starting up, in 3 seconds")
        await asyncio.sleep(3.0)
        print("Running...")

        # Create Notifier and assign it to a variable
        notifier = can.Notifier(bus, listeners, loop=asyncio.get_running_loop())

        try:
            # Start sending first message
            bus.send(can.Message(arbitration_id=0x1001))

            print("Bouncing 10 messages...")
            for _ in range(10):
                # Wait for next message from AsyncBufferedReader
                msg = await reader.get_message()
                # Delay response
                await asyncio.sleep(2.0)
                msg.arbitration_id += 1
                bus.send(msg)

            # Wait for last message to arrive
            await reader.get_message()
            print("Done!")
        finally:
            # Explicitly stop the notifier when done or if an error occurs
            notifier.stop()

if __name__ == "__main__":
    asyncio.run(main())