import code 
import copy
import sys
import rom_data
import tools

# code.interact(local=dict(globals(), **locals()))

def output_narc(rom, rom_name):
	return tools.output_narc("learnsets", rom, rom_name)

def write_readable_to_raw(file_name, narc_name="learnsets"):
	tools.write_readable_to_raw(file_name, narc_name, to_raw)

def to_raw(readable):
	raw = copy.deepcopy(readable)

	if rom_data.BASE_ROM == "HGSS" or rom_data.BASE_ROM == "PL":
		max_moves = 20
	else:
		max_moves = 25

	for n in range(max_moves):
		if f'move_id_{n}' in readable:
			
			if readable[f'move_id_{n}'] == "-":
				continue

			if readable[f'move_id_{n}'].split(" ")[0].lower() == "expanded":
				raw[f'move_id_{n}'] = int(readable[f'move_id_{n}'].split(" ")[-1])
			else:
				raw[f'move_id_{n}'] = rom_data.MOVES.index(readable[f'move_id_{n}'])

			#update index info for readable since ruby side only updates the name, not id
			readable[f'move_id_{n}_index'] = raw[f'move_id_{n}']

		if f'lvl_learned_{n}' in readable:
			raw[f'lvl_learned_{n}'] = readable[f'lvl_learned_{n}']
	
	return raw

################ If run with arguments #############

if len(sys.argv) > 2 and sys.argv[1] == "update":
	rom_data.set_global_vars(sys.argv[3])
	file_names = sys.argv[2].split(",")
	 
	for file_name in file_names:
		write_readable_to_raw(int(file_name))
	
