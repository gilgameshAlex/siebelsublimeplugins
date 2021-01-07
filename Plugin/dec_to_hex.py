import sublime
import sublime_plugin
import re


class DecToHexCommand(sublime_plugin.TextCommand):
	#def on_done (self, Regex):
	#	self.window.set_layout({
	#		"cols": [0, 0.5, 1],
	#		"rows": [0.0, 0.33, 0.66, 1.0],
	#		"cells": [[0,0,1,3], [1,0,2,1], [1,1,2,2], [1,2,2,3]]
	#		})
		
		

	MAX_STR_LEN = 10
	def run(self, edit):
		v = self.view
		i = 0
		resultStr = ""
		for region in v.sel():
			for line in v.lines(region):
				i = i + 1
				s = v.substr(line)
				s = s.replace('\n', '')
				match = re.search(r'Warning\s\d{1}\s([a-z0-9]{16}):\d{1}', s)
				if match:
					resultStr = resultStr + "\n[" + "line = " + str(i) + "] " + s;
				
				#s = s.replace('\n', '')
				#str1 = str1 + s + "INDEX=" + str(i)
		if resultStr:
			newView = v.window().new_file()
			newView.run_command("insert",{"characters": resultStr})
		
		sublime.status_message("Complete - DecToHexCommand")
		#sublime.status_message(str1)
		#---
		#dec = v.substr(v.sel()[0])
		#if dec.isdigit():
		#	v.replace(edit, v.sel()[0], hex(int(dec))[2:].upper())
		#else:
		#	if len(dec) > self.MAX_STR_LEN:
		#		logMsg = dec[0:self.MAX_STR_LEN]+"..."
		#	else:
		#		logMsg = dec
		#	sublime.status_message("\"" + logMsg + "\" isn't a decimal number!")
		#self.view.show_popup(v.substr(v.line(1,1)), sublime.HTML, location=-1, on_navigate=print)
		#str1 = v.substr(v.line(1)[0])
		#size1 = v.size()
		#sublime.status_message("size=" + str(size1)+"-str="+str(str1))
		#self.view.insert(edit, 0, "1")
		#self.window.focus_group(0)
		#self.view.insert(edit, 0, "2\n")
		#createdView = self.window.new_file()
		#self.view.insert(edit, 0, "3\n")
		#createdView.run_command("insert",{"characters": "Hello"})
		#self.view.insert(edit, 0, "4\n")
		#self.window.insert(0, createdView)
		#self.view.insert(edit, 0, "5\n")
		#self.view.insert(edit, 0, "123Hello, World!123")
		#self.view.insert(edit, 0, "Hello, World!")
		#self.view.show_popup('qweqweq', sublime.HTML, location=-1, on_navigate=print)
		