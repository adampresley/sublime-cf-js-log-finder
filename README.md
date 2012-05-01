# Sublime ColdFusion console/CFDUMP/CFABORT Finder

## About
Sublime ColdFusion console/CFDUMP/CFABORT Finder is a Sublime Text 2 plugin designed to allow
users an easy way to find code in ColdFusion and JavaScript source that may
contain commands like *console.log()*, *&lt;cfdump&gt;*, or *&lt;cfabort&gt;*.


## Installation
To "install" this plugin find your User Packages directory for Sublime. In Windows 7
this would be something to the effect of **C:\Users\me\AppData\Roaming\Sublime Text 2\Packages\User**.
For most *nix distributions that would be **/home/me/.conf/Sublime Text 2/Packages/User**.

Download the Python file for this project and place it in the above directory. This will load
up the plugin. Now you will need to have a key-binding so you can use it. In that same user
directory there should be *sublime-keymap* files for each OS. Open the one for your particular
operating system, and create the following:

    { "keys": [ "ctrl+alt+k" ], "command": "find_console_log" }

Of course be sure that if there are other key bindings to add a comma where
appropriate, as this object is technically being placed in an array with other
objects.

Don't like CTRL+ALT+K for the key binding? Change it right there! :)


## License

Sublime ColdFusion console/CFDUMP/CFABORT Finder
Copyright (C) 2011 Adam Presley

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

adam [at] adampresley [dot] com