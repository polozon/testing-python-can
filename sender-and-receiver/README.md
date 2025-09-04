# Sender and Receiver App

Här finns två appar. Använd tmux med två panes.
Först startas receiver_app och sedan startas sender_app.
Man kan se hur sändaren skickar och mottagaren tar emot dessa meddelanden

Testar så här:

```bash
tmux
C-b "
uv run receiver_app.py
C-b q 0
uv run sender_app.py 
```

Man kan också testa så här utan tmux, sender körs i bakgrunden:

```bash
uv run sender_app.py > /dev/null &
uv run receiver_app.py
Ctrl+C
fg
Ctrl+C
```
