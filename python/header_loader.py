import ndspy
import ndspy.rom
import ndspy.narc
import code 
import io
import codecs
import os
import json
import sys
import msg_reader
import msg_reader2
from header_reader import output_headers_json
from msg_reader2 import output_texts


# code.interact(local=dict(globals(), **locals()))


#################### CREATE FOLDERS #############################

rom_name = "projects/" + sys.argv[1].split(".")[0] 

# code.interact(local=dict(globals(), **locals()))

if not os.path.exists(f'{rom_name}'):
    os.makedirs(f'{rom_name}')

for folder in ["narcs", "texts", "json", "message_texts", "story_texts"]:
	if not os.path.exists(f'{rom_name}/{folder}'):
		os.makedirs(f'{rom_name}/{folder}')

################# HARDCODED ROM INFO ##############################

NARCS = [["a/0/1/2", "headers"],["a/0/0/2", "message_texts"], ["a/0/0/3", "story_texts"]]
BW_MSG_BANKS = [[89, "locations"]]
BW2_MSG_BANKS = [[109, "locations"]]
MSG_BANKS = []


################### EXTRACT RELEVANT BW_NARCS AND ARM9 #######################

narc_info = {} ##store narc names and file id pairs

with open(f'{rom_name.split("/")[-1]}.nds', 'rb') as f:
    data = f.read()

rom = ndspy.rom.NintendoDSRom(data)

if str(rom.name)[-3] == '2':
	narc_info["base_rom"] = "BW2"
	MSG_BANKS = BW2_MSG_BANKS
	narc_info["base_version"] = str(rom.name)[20] + "2"
else:
	narc_info["base_rom"] = "BW"
	MSG_BANKS = BW_MSG_BANKS
	narc_info["base_version"] = str(rom.name)[20]

# code.interact(local=dict(globals(), **locals()))

for narc in NARCS:
	file_id = rom.filenames[narc[0]]
	file = rom.files[file_id]
	narc_file = ndspy.narc.NARC(file)

	# extract text banks
	print(narc[1][-5:])
	if narc[1][-5:] == "texts":
		output_texts(f"{rom_name}/{narc[1]}", narc_file)


	narc_info[narc[1]] = file_id # store file ID for later
	
	with open(f'{rom_name}/narcs/{narc[1]}-{file_id}.narc', 'wb') as f:
	    f.write(file)

#############################################################

################### EXTRACT RELEVANT TEXTS ##################

msg_file_id = narc_info['message_texts']

for msg_bank in MSG_BANKS:
	text = msg_reader.parse_msg_bank(f'{rom_name}/narcs/message_texts-{msg_file_id}.narc', msg_bank[0])

	with codecs.open(f'{rom_name}/texts/{msg_bank[1]}.txt', 'w', encoding='utf_8') as f:
	    for block in text:
	    	for entry in block:
	    		try:
	    			f.write(entry)
	    		except UnicodeEncodeError:
	    			print("error")
	    			# f.write(str(entry.encode("UTF-8")))
	    		f.write("\n")


##############################################################
################### WRITE SESSION SETTINGS ###################

settings = {}
settings["rom_name"] = rom_name
settings.update(narc_info)

with open(f'session_settings.json', "w") as outfile:  
	json.dump(settings, outfile) 
	print(settings)

#############################################################
################### CONVERT TO JSON #########################

headers_narc_data = ndspy.narc.NARC(rom.files[narc_info["headers"]])
output_headers_json(headers_narc_data)




