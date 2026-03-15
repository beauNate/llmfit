#!/usr/bin/python3
"""Drive the llmfit TUI with simulated keypresses for demo recording."""
import pexpect
import time
import sys
import os
import signal
import threading

os.environ['TERM'] = 'xterm-256color'

p = pexpect.spawn('./target/release/llmfit', dimensions=(35, 100))

stop_reader = threading.Event()

def reader():
    while not stop_reader.is_set():
        try:
            data = p.read_nonblocking(size=4096, timeout=0.1)
            if data:
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
        except pexpect.TIMEOUT:
            pass
        except pexpect.EOF:
            break

reader_thread = threading.Thread(target=reader, daemon=True)
reader_thread.start()


def pause(secs=2):
    time.sleep(secs)


def send(key, delay=0.4):
    p.send(key)
    time.sleep(delay)


def send_text(text, char_delay=0.06):
    for ch in text:
        p.send(ch)
        time.sleep(char_delay)
    time.sleep(0.3)


# --- Wait for TUI to load ---
pause(3)

# --- 1. Browse the table ---
for _ in range(8):
    send('j', 0.25)
pause(1)

for _ in range(8):
    send('k', 0.2)
pause(1)

# --- 2. Search ---
send('/', 0.5)
send_text('llama 8b')
pause(1.5)
send('\x1b', 0.5)
pause(0.5)

# --- 3. Fit filter ---
send('f', 1)
send('f', 1)
send('f', 1)
send('f', 0.8)
send('f', 0.8)
send('f', 0.8)
pause(0.5)

# --- 4. Sort cycling ---
send('s', 1)
send('s', 1)
send('s', 1)
send('s', 0.8)
send('s', 0.8)
send('s', 0.8)
send('s', 0.8)
pause(0.5)

# --- 5. Detail view ---
send('\r', 0.5)
pause(2)
send('\x1b', 0.5)
pause(0.5)

# --- 6. Compare ---
send('m', 0.5)
for _ in range(3):
    send('j', 0.3)
send('c', 0.5)
pause(2)
send('\x1b', 0.5)
pause(0.5)

# --- 7. Visual multi-select ---
send('v', 0.5)
for _ in range(4):
    send('j', 0.3)
pause(0.5)
send('c', 0.5)
pause(2)
send('\x1b', 0.5)
pause(0.5)

# --- 8. Plan mode ---
send('p', 0.5)
pause(1.5)
send('\x15', 0.3)
send_text('16384', 0.08)
pause(1)
send('\t', 0.5)
pause(0.5)
send('\t', 0.5)
send('\x15', 0.3)
send_text('20', 0.08)
pause(1.5)
send('\x1b', 0.5)
pause(0.5)

# --- 9. Theme cycling ---
send('t', 1)
send('t', 1)
send('t', 1)
send('t', 1)
send('t', 1)
send('t', 0.8)
pause(1)

# --- 10. Provider filter ---
send('P', 0.5)
pause(1.5)
send('\x1b', 0.5)
pause(0.5)

# --- 11. Use case filter ---
send('U', 0.5)
pause(1.5)
send('\x1b', 0.5)
pause(1)

# --- Quit ---
send('q', 0.5)

stop_reader.set()
reader_thread.join(timeout=2)
try:
    p.expect(pexpect.EOF, timeout=3)
except pexpect.TIMEOUT:
    p.kill(signal.SIGTERM)
    time.sleep(0.5)
p.close()
