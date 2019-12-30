SSHTunneller is a simple docker image which allows you to establish SSH Tunnels by just deploying a container with some enviroment variables by password or publickey authentication. The SSH Tunnels are pure python implemented with the [SSHTunnel library](https://github.com/pahaz/sshtunnel). This little tool uses the magic of Docker to restart the tunnel if the tunnel dies for any reason.

## Table of contents
- [Usage scenario](#Usage-scenario)
- [Requirements](#Requirements)
- [Quick start](#quick-start)
- [Contributing](#contributing)
- [Thanks](#thanks)
- [Copyright and license](#copyright-and-license)

## Usage Scenario
A container may need to connect a port of a remote server (i.e. 8080) where only SSH port (usually port 22) is reachable. The container ports can be used as localhost ports mapped with the port mapping feature of Docker.
```
----------------------------------------------------------------------

                            |
-------------+              |    +----------+
    LOCAL    |              |    |  REMOTE  | :22 SSH
    CONTAINER| <===== SSH =====> |  SERVER  | :80 web service
-------------+              |    +----------+
                            |
                         FIREWALL (only port 22 is open)

----------------------------------------------------------------------
```

BTW, this amazing art and description has been modified from [SSHTunnel](https://github.com/pahaz/sshtunnel) scenario.

## Requirements

- SSH Endpoint with publickey-based or password-based auth.

## Quick start

The start is pretty simple, let's start with an example:

Modify the docker-compose provided below:
```yaml
version: '3.4'

services:
  sshtunneller:
    image: jossec101/sshtunneller
    container_name: sshtunneller
    hostname: sshtunneller
    ports:
      - "80:80"
      - "3306:3306"
    environment:
      - ssh_host=sshd_server_test
      - ssh_port=22
      - ssh_username=root
      #- ssh_password=This_Is_a_SSH_P4SSW0RD
      - ssh_private_key_password=12345
      - remote_bind_addresses=[("127.0.0.1", 80),("127.0.0.1", 3306)]
      - local_bind_addresses=[("0.0.0.0", 80),("0.0.0.0", 3306)]
    volumes: 
      - ./sshd_server_test/keys:/private.key
    restart: always
```
- Set the ssh_host (e.g. ssh.mycompany.com), ssh_port and ssh_username
- If you are using publickey-based authentication, mount a volume with the private key mapped to the file /private.key in the container and also set the ssh_private_key_password with the passphrase/password of the encrypted private key. ❗❗ *No test has been done* without an encrypted private key.❗❗
- If you are using password-based authentication, just set the ssh_password environment variable. If you mount a private key file as mentioned before, publickey-based authentication will be prioritized.
- Set the remote and local bind addresses, in this example the port 80 of the target machine is recreated in the port 80 of our local container. The same with the 3306. Pay attention to these python-based lists and tuples.

Finally, just set the shell to the docker-compose.yml file and:
```
docker-compose up -d
```

## Example test
A dummy docker-compose.yml file is located in this repository, this compose deploys a SSHD server with publickey authentication with example keys and the SSHTunneller for testing purposes. I used Windows so I couldn't use the panubo/sshd without permission issues, but you can use this image directly on Linux.

## Contributing 

Have a bug or a feature request? Issues and PRs are welcome! 😀

## Thanks

The code uses the great [SSHTunnel](https://github.com/pahaz/sshtunnel) for deploying SSHTunnels with Python.

## Copyright and license
Code released under the [MIT License](https://github.com/Jossec101/SSHTunneller/blob/master/LICENSE).

Enjoy 🎉