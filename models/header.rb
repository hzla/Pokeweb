class Header

	def self.get_all
		file_path = "#{$rom_name}/json/headers/headers.json"
		data = JSON.parse(File.open(file_path, "r"){|f| f.read})
		data
	end

	def self.location_names
		file_path = "#{$rom_name}/texts/locations.txt"
		data = File.open(file_path, "r:ISO8859-1"){|f| f.read}.split("\n").uniq
	end

	def self.find_location_by_map_id map_id
		headers = get_all
		location = nil
		script = nil
		text = nil
		headers.each do |k,v|
			next if k == "count"
			if v["overworlds_id"] == map_id
				location = v["location_name"]
				
				script = v["script_id"]
				text = v["text_bank_id"]
				p script
				break
			end
		end
		[location, script, text]
	end


	def self.write_batch_data data
		@@upcases = []
		data["file_names"].each do |file|
			data["file_name"] = file
			write_data(data)
		end
	end

	def self.write_data data, batch=false
		@@upcases = []
		if batch
			write_batch_data data
		end

		file_name = data["file_name"]
		field_to_change = data["field"]
		changed_value = data["value"]

		file_path = "#{$rom_name}/json/headers/headers.json"
		json_data = JSON.parse(File.open(file_path, "r"){|f| f.read})

		if data["int"]
			changed_value = changed_value.to_i
		end

		if data["field"] == "location_name"
			location_path = "#{$rom_name}/texts/locations.txt"
			location_names = File.open(location_path, "r:ISO8859-1"){|f| f.read}.split("\n")
			location_name_id = location_names.find_index(changed_value)
			json_data[file_name]['location_name_id'] = location_name_id
		end


		json_data[file_name][field_to_change] = changed_value
		File.open(file_path, "w") { |f| f.write json_data.to_json }
	end

	def self.expanded_fields
		col_1 = [[255, "map_type"], [255, "weather_id"], [65535, "overworlds_id"], [65535, "parent_map_id"], [65535, "texture_id"], [65535, "level_script_id"]]
		col_2 = [[255, "name_style_id" ], [65535, "name_icon"], [255, "camera_id"], [255, "flags"], [4294967296, "fly_x"], [4294967296, "fly_y"], [4294967296, "fly_z"]]
		col_3 = [[65535, "music_spring_id"], [65535,"music_summer_id"], [65535,"music_fall_id"], [65535,"music_winter_id"], [255,"unknown_1"], [255,"unknown_2"], [65535,"unknown_3"], [65535,"unknown_4"]]
		[col_1,col_2,col_3]
	end

	def self.hgss_expanded_fields
		col_1 = [[65535, "events_id"], [255, "area_data"], [65535, "map_info"]]
		col_2 = [[65536, "script_header_id" ],[255, "map_name_textbox_id"], [65535, "music_day"], [65535,"music_night"] ]
		col_3 = [[255, "weather"],[255, "camera"],[255, "follow_mode"],[255, "permissions"]]
		[col_1,col_2,col_3]
	end


end




