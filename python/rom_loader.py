import ndspy
import ndspy.rom, ndspy.codeCompression
import ndspy.narc
import code 
import io
import codecs
import os
import json
import sys
import msg_reader

from multiprocessing import Pool
import subprocess
from arm9_reader import output_tms_json



# code.interact(local=dict(globals(), **locals()))


#################### CREATE FOLDERS #############################
print("creating project folders")

narc_info = {} ##store narc names and file id pairs

with open(f'session_settings.json', "r") as outfile:  
	narc_info = json.load(outfile) 

rom_name = narc_info['rom_name'] 

# code.interact(local=dict(globals(), **locals()))

if not os.path.exists(f'{rom_name}'):
	os.makedirs(f'{rom_name}')

for folder in ["narcs", "texts", "json"]:
	if not os.path.exists(f'{rom_name}/{folder}'):
		os.makedirs(f'{rom_name}/{folder}')



################# HARDCODED ROM INFO ##############################

BW_NARCS = [["a/0/1/6", "personal"],
["a/0/0/9", "matrix"], 
["a/1/2/5", "overworlds"],
["a/0/1/7", "growth"],
["a/0/1/8", "learnsets"],
["a/0/1/9", "evolutions"], 
["a/0/2/0", "babyforms"],
["a/0/2/1","moves"],
["a/0/2/4", "items"],
["a/0/9/2", "trdata"],
["a/0/9/3", "trpok"],
["a/1/2/6", "encounters"],
["a/0/0/3", "storytext"],
["a/0/5/6", "scripts"],
["a/0/0/4", "sprites"],
["a/0/0/7", "icons"]]

BW_MSG_BANKS = [[286, "moves"],
[285, "abilities"],
[284, "pokedex"],
[191, "tr_classes"],
[190, "tr_names"],
[54, "items"]]

BW2_NARCS = [["a/0/1/6", "personal"],
["a/0/0/9", "matrix"], 
["a/1/2/6", "overworlds"],
["a/0/1/7", "growth"],
["a/0/1/8", "learnsets"],
["a/0/1/9", "evolutions"], 
["a/0/2/0", "babyforms"],
["a/0/2/1","moves"],
["a/0/2/4", "items"],
["a/0/9/1", "trdata"],
["a/0/9/2", "trpok"],
["a/1/2/7", "encounters"],
["a/0/0/3", "storytext"],
["a/0/5/6", "scripts"],
["a/2/8/2", "marts"],
["a/2/8/3", "mart_counts"],
["a/2/7/3", "grottos"],
["a/0/0/4", "sprites"],
["a/0/0/7", "icons"]]

BW2_MSG_BANKS = [[488, "moves"],
[487, "abilities"],
[486, "pokedex"],
[383, "tr_classes"],
[382, "tr_names"],
[64, "items"]]

NARCS = []
MSG_BANKS = []

################### EXTRACT RELEVANT NARCS AND ARM9 #######################

if narc_info["base_rom"] == "BW":
	MSG_BANKS = BW_MSG_BANKS
	NARCS = BW_NARCS
else:
	MSG_BANKS = BW2_MSG_BANKS
	NARCS = BW2_NARCS

print("extracting narcs")

with open(f'{rom_name.split("/")[-1]}.nds', 'rb') as f:
	data = f.read()

rom = ndspy.rom.NintendoDSRom(data)

for narc in NARCS:
	file_id = rom.filenames[narc[0]]
	file = rom.files[file_id]
	parsed_file = ndspy.narc.NARC(file)
	
	narc_info[narc[1]] = file_id # store file ID for later
	
	with open(f'{rom_name}/narcs/{narc[1]}-{file_id}.narc', 'wb') as f:
		f.write(file)


print("decompressing arm9")

arm9 = ndspy.codeCompression.decompress(rom.arm9)

with open(f'{rom_name}/arm9.bin', 'wb') as f:
	f.write(arm9)


#############################################################

################### EXTRACT RELEVANT TEXTS ##################
print("parsing texts")

msg_file_id = narc_info['message_texts']

for msg_bank in MSG_BANKS:
	text = msg_reader.parse_msg_bank(f'{rom_name}/narcs/message_texts-{msg_file_id}.narc', msg_bank[0])
	with codecs.open(f'{rom_name}/texts/{msg_bank[1]}.txt', 'w', encoding='utf_8') as f:
		for block in text:
			for entry in block:
				try:
					f.write(entry)
				except UnicodeEncodeError:
					print("text parse error")
					# f.write(str(entry.encode("UTF-8")))
				f.write("\n")


##############################################################
################### WRITE SESSION SETTINGS ###################

settings = {}
settings.update(narc_info)
settings["output_arm9"] = True



with open(f'session_settings.json', "w+") as outfile:  
	json.dump(settings, outfile) 

#############################################################
################### Provision Placeholders for alt form sprites ###########


if narc_info["base_rom"] == "BW2":
	# sprites
	sprite_file_path = f'{rom_name}/narcs/sprites-{settings["sprites"]}.narc'
	narc = ndspy.narc.NARC.fromFile(sprite_file_path)

	while len(narc.files) < 15080:
		narc.files.append(narc.files[-1])

	placeholder_sprites = narc.files[15000:15020]

	
	for n in range(100):
		narc.files += placeholder_sprites

	with open(f'{rom_name}/narcs/sprites-{settings["sprites"]}.narc', 'wb') as f:
		f.write(narc.save())

	# party icons 
	sprite_file_path = f'{rom_name}/narcs/icons-{settings["icons"]}.narc'
	narc = ndspy.narc.NARC.fromFile(sprite_file_path)

	while len(narc.files) < 1516:
		narc.files.append(narc.files[-1])

	placeholder_sprites = narc.files[1502:1504]

	
	for n in range(100):
		narc.files += placeholder_sprites

	with open(f'{rom_name}/narcs/icons-{settings["icons"]}.narc', 'wb') as f:
		f.write(narc.save())



	



#############################################################
####################CONVERT TO JSON #########################


os.system("python python/parallel.py")

output_tms_json(arm9)

