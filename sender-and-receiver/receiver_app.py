import can

def receive_can_messages():
    """Listens for and prints CAN messages from the vcan0 interface."""
    try:
        # Connect to the vcan0 interface
        bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
        
        print("Listening for CAN messages on vcan0...")
        for msg in bus:
            print(f"Received message: {msg}")

    except can.exceptions.CanError as e:
        print(f"Error receiving message: {e}")
    except KeyboardInterrupt:
        print("Receiver stopped by user.")
    finally:
        if 'bus' in locals():
            bus.shutdown() # Properly close the bus

if __name__ == "__main__":
    receive_can_messages()
