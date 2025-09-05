#!/usr/bin/env python

"""
This example demonstrates how to use async IO with python-can.
"""

import asyncio
import os
import errno
from typing import TYPE_CHECKING

import can

if TYPE_CHECKING:
    from can.notifier import MessageRecipient


def print_message(msg: can.Message) -> None:
    """Regular callback function. Can also be a coroutine."""
    print(msg)

async def read_can_messages(reader: can.AsyncBufferedReader, bus: can.Bus, queue: asyncio.Queue) -> None:
    print("Listening on CAN messages...")
    try:
        while True:
            msg = await reader.get_message()
            print(f"Received CAN message: {msg}")
            # Only bounce if arbitration_id is 20
            if msg.arbitration_id == 20:
                msg.arbitration_id += 1
                bus.send(msg)
                await queue.put(f"CAN message bounced: {msg}")
            # If arbitration_id is 10, trigger a command via the queue
            if msg.arbitration_id == 10:
                await queue.put("CAN trigger: send 0x200 8 7 6")
    except asyncio.CancelledError:
        print("CAN message reader stopped.")

async def read_commands_from_pipe(pipe_path: str, queue: asyncio.Queue) -> None:
    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)
    print(f"Listening for commands on named pipe: {pipe_path}")
    try:
        while True:
            try:
                fd = os.open(pipe_path, os.O_RDONLY | os.O_NONBLOCK)
                with os.fdopen(fd) as fifo:
                    while True:
                        line = await asyncio.to_thread(fifo.readline)
                        if not line:
                            break  # Writer closed; reopen pipe
                        cmd = line.strip()
                        if cmd:
                            await queue.put(f"Pipe command: {cmd}")
            except OSError as e:
                if e.errno == errno.ENXIO:
                    # No writer present, sleep and retry
                    await asyncio.sleep(0.5)
                else:
                    print(f"Pipe error: {e}")
                    await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        print("Pipe command reader stopped.")

async def process_queue(queue: asyncio.Queue, bus: can.Bus) -> None:
    print("Processing queue...")
    try:
        while True:
            item = await queue.get()
            print(f"Queue received: {item}")
            # Handle send command from pipe or CAN trigger
            if "send " in item:
                parts = item.split()
                if len(parts) >= 4:
                    try:
                        arbitration_id = int(parts[2], 0)
                        data = [int(x, 0) for x in parts[3:]]
                        msg = can.Message(arbitration_id=arbitration_id, data=bytearray(data))
                        bus.send(msg)
                        print(f"Sent CAN message: {msg}")
                    except Exception as e:
                        print(f"Error sending CAN message: {e}")
                else:
                    print("Invalid send command format.")
            queue.task_done()
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        print("Queue processor stopped.")

async def main() -> None:
    pipe_path = "/tmp/can_commands"
    queue = asyncio.Queue()

    with can.Bus(
        interface="socketcan", channel="vcan0", receive_own_messages=True
    ) as bus:
        reader = can.AsyncBufferedReader()
        logger = can.Logger("logfile.asc")

        listeners: list["MessageRecipient"] = [
            print_message,
            reader,
            logger,
        ]

        print("Starting up, in 3 seconds")
        await asyncio.sleep(3.0)
        print("Running...")

        notifier = can.Notifier(bus, listeners, loop=asyncio.get_running_loop())

        try:
            bus.send(can.Message(arbitration_id=0x1001))

            read_task = asyncio.create_task(read_can_messages(reader, bus, queue))
            pipe_task = asyncio.create_task(read_commands_from_pipe(pipe_path, queue))
            queue_task = asyncio.create_task(process_queue(queue, bus))

            tasks = [read_task, pipe_task, queue_task]
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            print("Main cancelled.")
        finally:
            notifier.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user. Shutting down gracefully.")