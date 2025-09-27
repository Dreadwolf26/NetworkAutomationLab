import os, yaml, paramiko
from dotenv import load_dotenv

load_dotenv()

hostname = os.getenv("PI_NAME")
username = os.getenv("PI_USER")
password = os.getenv("PI_PASS")

#opening playbook to read data
def run_playbook(playbook_id: str):
    with open("playbooks.yaml", "r") as f:
        data = yaml.safe_load(f)
    playbooks = {pb["id"]: pb for pb in data["playbooks"]}
    #graceful failure if playbook_id is not found
    if playbook_id not in playbooks:
        raise ValueError(f"Playbook {playbook_id} not found")

    playbook = playbooks[playbook_id]
    #connect to the raspberry Pi using Paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #print("DEBUG:", hostname, username, password) # Debugging line to check connection parameters
    ssh.connect(hostname, username=username, password=password)


    # Execute the commands in the playbook
    results = []
    for c in playbook["commands"]:
        cmd = c["cmd"]
        desc = c.get("description", "")
        _, stdout, _ = ssh.exec_command(cmd)
        results.append({"cmd": cmd, "desc": desc, "output": stdout.read().decode()})


    ssh.close()
    #store the output if specified in the playbook
    if "store_output" in playbook and playbook["store_output"]:
        with open(playbook["store_output"], "w") as f:
            for r in results:
                f.write(f"$ {r['cmd']}\n{r['output']}\n")

    return results
