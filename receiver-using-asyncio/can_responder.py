
import asyncio
import can

async def main():
    """
    Listens for CAN messages on vcan0 and responds to messages with ID 10.
    """
    with can.Bus(interface='socketcan', channel='vcan0') as bus:
        reader = can.AsyncBufferedReader()
        notifier = can.Notifier(bus, [reader])
        print("Listening for CAN messages on vcan0...")
        async for msg in reader:
            print(f"Received message: {msg}")
            if msg.arbitration_id == 10:
                print(f"Received message with ID 10: {msg}")
                response_msg = can.Message(
                    arbitration_id=11,
                    data=[0xDE, 0xAD, 0xBE, 0xEF],
                    is_extended_id=False
                )
                try:
                    bus.send(response_msg)
                    print(f"Sent message with ID 11: {response_msg}")
                except can.CanError:
                    print("Failed to send message")
        print("Shutting down...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped by user")
