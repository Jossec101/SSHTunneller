from sshtunnel import open_tunnel
from time import sleep
import sys
import os
import ast
import logging
import io
from contextlib import redirect_stdout
#Logger
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',level=logging.INFO)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

### Setup the console handler with a StringIO object
log_capture_string = io.StringIO()
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.ERROR)

### Add the console handler to the logger
logger.addHandler(ch)


logging.info("Logger set!")

logging.info("SSH Tunnel starting...")

def main():
    #Env variables
    ssh_host = os.environ.get("ssh_host")
    ssh_port = os.environ.get("ssh_port")
    ssh_username = os.environ.get("ssh_username")
    ssh_password = os.environ.get("ssh_password")
    ssh_private_key_password = os.environ.get("ssh_private_key_password")
    remote_bind_addresses = os.environ.get("remote_bind_addresses")
    local_bind_addresses = os.environ.get("local_bind_addresses")
    
    private_key_dir = "/private.key"
    if os.path.exists(private_key_dir):
        logging.info("Private key found, certificate mode enabled")
        if ssh_private_key_password is None:
            logging.error("Private key password not set, please set it as an environment variable: ssh_private_key_password")
            sys.exit(-1)
    elif ssh_password is None:
        logging.error("SSH Password not provided, quitting...")
        sys.exit(-1)

    
    

    if os.path.exists(private_key_dir):
        try:
            with open_tunnel(
            (ssh_host, int(ssh_port)),
            ssh_username=ssh_username,
            ssh_pkey=private_key_dir,
            ssh_private_key_password=ssh_private_key_password,
            remote_bind_addresses=ast.literal_eval(remote_bind_addresses),
            local_bind_addresses=ast.literal_eval(local_bind_addresses),
            set_keepalive=30.0
            ) as server:
                logging.info(f"SSH Tunnels established on {ssh_username}@{ssh_host}:  remote_bind_addresses:{remote_bind_addresses}, local_bind_addresses:{local_bind_addresses}")
                while True:
                    CheckTunnel(server,log_capture_string)
            
        except Exception as e:
            logging.error("SSH Tunnel Failed!")
            logging.error(e)
        
        finally:
            logging.warning("SSH Tunnel ended")
    else:
        try:
            with open_tunnel(
            (ssh_host, int(ssh_port)),
            ssh_username=ssh_username,
            ssh_password=ssh_password,
            remote_bind_addresses=ast.literal_eval(remote_bind_addresses),
            local_bind_addresses=ast.literal_eval(local_bind_addresses),
            set_keepalive=30.0
            ) as server:
                logging.info(f"SSH Tunnels established on {ssh_username}@{ssh_host}:  remote_bind_addresses:{remote_bind_addresses}, local_bind_addresses:{local_bind_addresses}")
                while True:
                    CheckTunnel(server,log_capture_string)
            
        except Exception as e:
            logging.error("SSH Tunnel Failed!")
            logging.error(e)
        
        finally:
            logging.error("SSH Tunnel ended")
            sys.exit(-2)


def CheckTunnel(server, stdout):
    #Check for remote side error from internal modules of Paramiko/SSHTunnel
    out = stdout.getvalue()

    if 'to remote side of the tunnel' in out:
        logging.error("Problem with remote side, maybe the other side is unavailable, restarting...")

        sys.exit(-2)

    server.check_tunnels()

    for x in server.tunnel_is_up.values():
        if(x is False):
            logging.error("Tunnel is dead, restarting...")
            sys.exit(-1)
    sleep(1)
    

if __name__== "__main__":
   main()
