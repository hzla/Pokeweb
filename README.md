
# Pokeweb: A GenV Rom Editor

## Features

Pokeweb is currently  able to edit map headers, items, personals, level-up learnsets, tm/tutor learnsets, tms, moves, encounters, trainers, evolutions, marts, grottos.

To be implemented editors are texts, battle subway trainers, PWT trainers, tutor moves, and OW events. 

You can join this Pokemon DS Rom Hacking discord server for updates as well as general support for your Pokemon gen IV/V rom hacking needs. [https://discord.gg/cTKQq5Y](https://discord.gg/cTKQq5Y)
## Windows Installation 

Click the WINDOWS_INSTALL.bat file which will run the included ruby and python installers and the commands for installing the required gems and python modules. 

If you already are using ruby >2.6 and python > 3.6, you can cancel the installers and the WINDOWS_INSTALL.bat will go straight to installing gems and python modules.

The Pokeweb server can then be started by clicking and running Pokeweb_Windows.bat. You should be able to view Pokeweb on localhost:4567 in your browser


### Manual Windows Install

If you are running into issues, try manually installing by clicking and running the ruby and python installers individually. Make sure both versions are in use. If the included installers fail, you can download download windows ruby installer [here](https://rubyinstaller.org/downloads/) and python installer [here](
).
You can check your version by typing 

 	$ ruby -v
and 
	$ python -V

Next, navigate to the Pokeweb root folder in cmd or powershell and run

	$ bundle install

followed by
	
    $ pip install ndspy

If the above steps succeed the server can now be run by running 

	$ ruby routes.rb

or by clicking and running Pokeweb_Windows.bat

## Mac OS Installation

Mac OS already comes with both ruby and python but you will need to update them to newer versions to run Pokeweb if you don't already have ruby >2.6 and python > 3.6. 

The easiest way to do this is to install [Homebrew](https://brew.sh/).
And then to follow these guides to update ruby and python.

[Installing Ruby on MacOS](https://stackify.com/install-ruby-on-your-mac-everything-you-need-to-get-going/)

[Installing Python on MacOS](https://opensource.com/article/19/5/python-3-default-mac)

Once they are installed, navigate to the project folder in Terminal.app 


	$ bundle install

followed by
	
    $ pip install ndspy

If the above steps succeed the server can now be run by running 

	$ ruby routes.rb



## Getting Started

Place any roms you wish to edit in root folder of Pokeweb and they should show up in the Load Rom dropdown on the homepage. Loading a rom will take you to the a map headers list for the rom while the rest of the editors load in the background. This can take anywhere between 5-15 seconds. In the future you can select an already loaded rom in the Load Project dropdown.

The rest is pretty simple.
<span align="r" style="color:  #1abc9c">
	Any thing this color can be clicked to be edited. 
</span>
If you make an invalid edit the border will turn <span style="color: #ff5555">red</span>, otherwise, your edits are saved automatically. 

To view a history of your edits, go to the Logs tab in the navbar on the rop right.

## Contributing

A rough overview of the app detailing what overall structure as well as planned todos can be found in misc/app_info.txt

## Contributing 

Thanks to kaphotics, andibad, bond697 for their posts on the project pokemon forums that helped with much of the format info for the narcs.

Thanks to turtleisaac for pokeditor src code that let me look up what some of bitfields did what as well for his partial list of move effects. 

Thanks to platinummaster for helping with my text parser algorithm

Thanks to Drayano for his forum post on the hidden grotto narc format.

Thanks to Spike-Eared Pichu for SDSME which helped me obtain some text banks and which I used as reference for the encounter editor.

Thanks to Mero Mero for info on where to find the tm list in the arm9


## License

Pokeweb is released under the [MIT License](https://opensource.org/licenses/MIT).