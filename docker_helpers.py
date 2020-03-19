import os
import sys

def shell():
    os.system('docker exec -it app /bin/bash')

def db_migrate(message):
	os.system(f"""docker container exec app flask db migrate -m "{message}" """)

def db_upgrade():
	os.system(f"""docker container exec app flask db upgrade """)
	

command_map = {
	'db_migrate': db_migrate,
	'db_upgrade': db_upgrade,
	'shell': shell
}


args = sys.argv
command_name = args[1]
command_args = args[2:]


if __name__ == "__main__":
    command_map[command_name](*command_args)
