# Gunicorn Configuration File
# https://docs.gunicorn.org/en/stable/settings.html

import os
import multiprocessing

# Server Socket
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"

# Worker Processes
# Rule of thumb: 2-4 workers per core
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5

# Server Mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging
errorlog = '-'
loglevel = os.getenv('LOG_LEVEL', 'info')
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process Naming
proc_name = 'knowledge-repo-server'

# Server Hooks
def on_starting(server):
    print("🚀 Gunicorn starting...")

def on_exit(server):
    print("👋 Gunicorn shutting down...")

def worker_int(worker):
    print(f"Worker received INT or QUIT signal: {worker.pid}")
