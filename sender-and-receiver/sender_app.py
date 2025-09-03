import can
import time

def send_can_messages():
    """Sends CAN messages to the vcan0 interface."""
    try:
        # Connect to the vcan0 interface
        bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

        message_count = 0
        while True:
            # Create a CAN message with an incrementing data payload
            msg = can.Message(
                arbitration_id=0x123,  # Standard CAN ID
                data=[message_count % 256, 0xDE, 0xAD, 0xBE, 0xEF, 0x00, 0x00, 0x00],
                is_extended_id=False
            )

            # Send the message
            bus.send(msg)
            print(f"Sent message: {msg}")

            message_count += 1
            time.sleep(1) # Wait for 1 second

    except can.exceptions.CanError as e:
        print(f"Error sending message: {e}")
    except KeyboardInterrupt:
        print("Sender stopped by user.")
    finally:
        if 'bus' in locals():
            bus.shutdown() # Properly close the bus

if __name__ == "__main__":
    send_can_messages()
