# Ansible Server Provisioning

This directory contains all ansible configurations.

## Host requirement

- **A Unix-like environment**
    - Linux or macOS
    - [WSL](https://docs.microsoft.com/en-us/windows/wsl/about) (WSL2 is tested)
- Python (Python3 preferred)
- Ansible 2.10+
    - `pip3 install ansible` or `pip install ansible`
- Ansible community package for docker commands
    - `ansible-galaxy collection install community.general`

## Node requirement

- Two servers with reasonable amount of resources
    - Do not try on free cloud VM with shared half-core CPU and 256 MB memory, processes or VM or both will be killed
    - A lot of cloud services provide free credits upon registration
- Ubuntu
    - 20.04 LTS preferred and tested (Focal)
    - Has python3 interpreter as default, eaiser for ansible to execute docker related components
- Ensure user `runner` is present in group `runner` **with `sudo` privilege without password**.
- SSH access.
    - **Add SSH public key to user `runner` on server.**

## Server Security before getting started

- Change configuration for common ports to higher
  For example:
    - Modify SSH port to be 50022
    - Use 50080 for all HTTP traffic
- Setup firewall to only allow traffic on specific ports
    - **Double check that modified SSH port is allowed**
    - Sometimes it may be even better to disable all public traffic
- Disable password login for root account
    - Upload public key to root account
    - Or just `sudo`

## Start provisioning

- Verify asnible is working and nodes are reachable
    ```sh
    ansible all -i repo/integration -m ping
    ```
  `"ping": "pong"` should be appearing twice as part of the message
- Play!
    ```sh
    ansible-playbook -i repo/integration backend.yml
    ansible-playbook -i repo/integration elasticsearch.yml
    ```
  Everything should be green or orange, the failed number on summary should be 0
    - Report an issue if it is not!

## Future goals

- **Add NGINX to rewrite requests paths and HTTPS**
- Manage users, public keys, permissions
- Automatically run backend and elasticsearch services and verify them
- Dockerize python backend server
- (Possibly) integrate deployment
