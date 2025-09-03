# testing-python-can

Provar vcan hemma

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

Skapade uv projekt: 

```bash
uv init --python 3.10
uv add python-can
```

