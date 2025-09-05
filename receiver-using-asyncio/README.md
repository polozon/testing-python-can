# Appar byggda med asyncio

Starta vcan på target genom att kopiera setup_vcan.sh dit och gör source

```bash
scp setup_vcan.sh root@10.42.0.126:~
ssh root@10.42.0.126
source ./setup_vcan.sh
```

Det är viktigt att skapa en Notifier om man ska kunna höra något
https://python-can.readthedocs.io/en/stable/notifier.html

Send this to the apps

```bash
cansend vcan0 00A#1122
candump vcan0
```

