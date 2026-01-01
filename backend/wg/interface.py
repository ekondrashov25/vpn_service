import subprocess

WG_INTERFACE = "wg0"

def run(cmd: list[str]) -> str:
    subprocess.run(cmd, check=True)
    
    
def interface_up():
    run(["wg-quick", "up", WG_INTERFACE])
    

def interface_down():
    run(["wg-quick", "down", WG_INTERFACE])
    

def show():
    result = subprocess.run(
        ["wg", "show", WG_INTERFACE],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout