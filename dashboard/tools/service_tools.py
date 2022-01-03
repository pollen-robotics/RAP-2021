"""Service management tools for RAP-2021."""
from subprocess import run, PIPE


def list_services():
    pipe1 = run(['systemctl list-unit-files'], stdout=PIPE, shell=True)
    pipe2 = run(['grep reachy'], input=pipe1.stdout, stdout=PIPE, shell=True)
    pipe3 = run(["awk '{print $1}'"], input=pipe2.stdout, stdout=PIPE, shell=True)

    output = pipe3.stdout.decode().split('\n')
    service_list = [service for service in output if service]
    return [srv_name.split('.service')[0] for srv_name in service_list]

def restart_service(service: str):
    run([f'sudo systemctl restart {service}.service'], stdout=PIPE, shell=True)


def stop_service(service: str):
    run([f'sudo systemctl stop {service}.service'], stdout=PIPE, shell=True)
