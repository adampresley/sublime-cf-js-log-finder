import os
import re
import sublime
import sublime_plugin

OUTPUT_VIEW_NAME = 'findconsolelog_result_view'

class FindConsoleLogCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.filePath = self.window.active_view().file_name()
		self.fileName = os.path.basename(self.filePath)

		self.patterns = [
			r"(console\.log\(.*?\))",
			r"(<cfdump|writedump)(.*?)(>|;)",
			r"(<cfabort|abort)(.*?)(>|;)"
		]

		self.configureOutputView()
		self.searchAndDestroy(self.filePath)
		self.showView()


	def searchAndDestroy(self, file):
		print "Starting dump search (console.log, cfdump, etc...) search..."
		self.writeToView(">> Starting dump search (console.log, cfdump, etc...) search...\n\n")

		lineNum = 0
		f = open(file, "r")

		#
		# Search each line for patterns of items we wish to target 
		#
		for line in f:
			lineNum += 1

			for pattern in self.patterns:
				for match in re.finditer(pattern, line, re.IGNORECASE):
					msg = "Match located: %s:%s : %s" % (lineNum, match.start(), match.group(0))
					self.writeToView(msg + "\n")

		f.close()
		self.writeToView(">> Complete.\n")


	def configureOutputView(self):
		if not hasattr(self, 'outputView'):
			self.outputView = self.window.get_output_panel(OUTPUT_VIEW_NAME)
			self.outputView.set_name(OUTPUT_VIEW_NAME)

		self.clearView()
		self.outputView.settings().set("file_path", self.filePath)


	def clearView(self):
		self.outputView.set_read_only(False)

		edit = self.outputView.begin_edit()
		self.outputView.erase(edit, sublime.Region(0, self.outputView.size()))
		self.outputView.end_edit(edit)
		self.outputView.set_read_only(True)


	def writeToView(self, msg):
		self.outputView.set_read_only(False)

		edit = self.outputView.begin_edit()
		self.outputView.insert(edit, self.outputView.size(), msg)

		self.outputView.end_edit(edit)
		self.outputView.set_read_only(True)


	def showView(self):
		self.window.run_command("show_panel", { "panel": "output." + OUTPUT_VIEW_NAME })


class FindConsoleLogEventListener(sublime_plugin.EventListener):
	disabled = False

	def __init__(self):
		self.previousInstance = None
		self.file_view = None

	def on_selection_modified(self, view):
		if FindConsoleLogEventListener.disabled:
			return

		if view.name() != OUTPUT_VIEW_NAME:
			return

		region = view.line(view.sel()[0])

		#
		# Make sure call once.
		#
		if self.previousInstance == region:
			return

		self.previousInstance = region

		#
		# Extract line from console result.
		#
		text = view.substr(region).split(":")
		if len(text) < 3:
			return

		#
		# Highlight the selected line
		#
		line = text[1].strip()
		col = text[2].strip()
		view.add_regions(OUTPUT_VIEW_NAME, [ region ], "comment")

		#
		# Find the file view.
		#
		filePath = view.settings().get("file_path")
		window = sublime.active_window()
		fileView = None

		for v in window.views():
			if v.file_name() == filePath:
				fileView = v
				break
		
		if fileView == None:
			return

		self.file_view = fileView
		window.focus_view(fileView)
		fileView.run_command("goto_line", {"line": line})
		fileRegion = fileView.line(fileView.sel()[0])

		# highlight file_view line
		fileView.add_regions(OUTPUT_VIEW_NAME, [ fileRegion ], "string")


	def on_deactivated(self, view):
		if view.name() != OUTPUT_VIEW_NAME:
			return

		self.previousInstance = None

		if self.file_view:
			self.file_view.erase_regions(OUTPUT_VIEW_NAME)
