# testing-python-can

Applikationer som provar socketcan på Ubuntu PC.
Eftersom man inte har ett riktig CAN-interface så används vcan0 istället.

Instruktion för att aktivera vcan, se
https://netmodule-linux.readthedocs.io/en/latest/howto/can.html

Aktiverade vcan på mini-silver-hp

```bash
sudo modprobe vcan
lsmod | grep vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 mtu 16
sudo ip link set up vcan0
ifconfig
```

Skapade uv projekt som innehåller python-can 

```bash
uv init --python 3.10
uv add python-can
```

Sedan kan man gå till sender-and-receiver, läs README.md och följ instruktionerna.

Installerade can-utils med: `sudo apt install can-utils`
