import ndspy
import ndspy.rom, ndspy.codeCompression
import ndspy.narc
import code 
import io
import codecs
import os
import os.path
from os import path
import json
import sys
import traceback

import personal_writer
import learnset_writer
import move_writer
import tm_writer
import header_writer
import encounter_writer
import trdata_writer
import trpok_writer
import item_writer
import evolution_writer
import overworld_writer
import text_writer

# code.interact(local=dict(globals(), **locals()))

# _writer files to run
narcs = ["personal","text", "learnset","move","header","encounter","trdata","trpok","item","evolution", "overworld"]
bw_narcs = ["mart" , "grotto"]

try: 
	rom_name = sys.argv[1].split(".")[0] 

	####################################################################
	################### WRITE NARCS/ARM9 TO ROM ############################
	with open(f"{rom_name.split('/')[1]}.nds", 'rb') as f:
	    data = f.read()
	rom = ndspy.rom.NintendoDSRom(data)

	settings = {}
	file_ids = {}
	with open(f'{sys.argv[1]}/session_settings.json', "r") as outfile:  
		settings = json.load(outfile)
		edited = settings["edited"] if "edited" in settings else []
		
		#run text and script exporters if true
		if settings["enable_single_npc_dbl_battles"] == True:
			edited.append("text")


		if settings["output_overworlds"] == False:
			narcs.remove("overworld")
		
		if settings["base_rom"] == "BW2":
			import mart_writer
			import grotto_writer
			narcs += bw_narcs

		#only output edited narcs
		narcs = list(set(narcs) | set(edited))


		if settings["output_arm9"] == True:
			tm_writer.output_arm9()
			mutable_rom = bytearray(data)
			arm9_offset = 16384 #0x4000

			#get edited arm9
			edited_arm9_file = bytearray(open(f'{rom_name}/arm9.bin', 'rb').read())

			# #compress it
			print ("compressing arm9")
			arm9 = bytearray(ndspy.codeCompression.compress(edited_arm9_file, isArm9=True))

			#reinsert arm9
			mutable_rom[arm9_offset:arm9_offset + len(arm9)] = arm9

			#update rom in memory
			rom = ndspy.rom.NintendoDSRom(mutable_rom)

			if settings["base_rom"] == "BW2":

				grotto_odds = 0
				grotto_odds = open(f'{rom_name}/grotto_odds.bin','rb').read()

				#load decompressed overlay
				overlay36 = rom.loadArm9Overlays([36])[36]
				
				#set data
				overlay36_data = overlay36.data
				B2_GROTTO_ODDS_OFFSET = 0x00055218
				W2_GROTTO_ODDS_OFFSET = 0x00055218 - 12

				if narc_info["base_version"] == "B2":
					GROTTO_ODDS_OFFSET = B2_GROTTO_ODDS_OFFSET
				else:
					GROTTO_ODDS_OFFSET = W2_GROTTO_ODDS_OFFSET

				
				# overwrite data with edits
				overlay36_data[GROTTO_ODDS_OFFSET:(GROTTO_ODDS_OFFSET + 200)] = grotto_odds
				
				#set new data
				overlay36.data = overlay36_data

				# recompress and insert
				rom.files[36] = overlay36.save(compress=True)
		
		for narc in narcs:
			rom = eval(f'{narc}_writer.output_narc(rom, rom_name)')

				
	##### save rom to exports
	if path.exists(f'exports'):
		rom.saveToFile(f"exports/{rom_name.split('/')[1]}.nds")
	else:
		os.makedirs('exports')
		rom.saveToFile(f"exports/{rom_name.split('/')[1]}.nds")

	print("Save 200 OK")
except:
	print("Save Failed")
	print(traceback.format_exc())
	
