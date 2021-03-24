class Pokenarc
	@@narc_name = ""
	@@upcases = []


	def self.get_data(file_name)
		JSON.parse(File.open(file_name, "r"){|f| f.read})["readable"]
	end

	def self.get_all 
		collection = []
		files = Dir["#{$rom_name}/json/#{@@narc_name}/*.json"]
		file_count = files.length

		(0..file_count - 1).each do |n|
			
			file = File.open("#{$rom_name}/json/#{@@narc_name}/#{n}.json", "r:ISO8859-1") {|f| f.read }
			json = JSON.parse(file)
			entry = json["readable"]

			collection[n] = entry
		end
		collection
	end

	def self.write_data data
		file_name = data["file_name"]
		field_to_change = data["field"]
		changed_value = data["value"]

		file_path = "#{$rom_name}/json/#{@@narc_name}/#{file_name}.json"
		json_data = JSON.parse(File.open(file_path, "r") {|f| f.read})

		if data["int"]
			changed_value = changed_value.to_i
		end

		if @@upcases == "all" || @@upcases.any? {|field| field.include? data["field"]} 
			changed_value = changed_value.upcase
		end

		if data["field"] == "class" && @@narc_name == "trdata"
			class_data = changed_value.split(" (")
			changed_value = class_data[0]
			
			new_class_id = class_data[1].split(")")[0]
			json_data["readable"]["class_id"] = new_class_id
		end


		json_data["readable"][field_to_change] = changed_value
		File.open(file_path, "w") { |f| f.write json_data.to_json }
	end


end