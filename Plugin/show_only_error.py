import sublime
import sublime_plugin
import re
import datetime

class ShowOnlyErrorCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        v = self.view
        resultStr = ""
        startTime = datetime.datetime.now()
        regions = v.find_all(r'(Export Failed)|(Symbolic String not found)|(\b(Error\s+\d+)|(GenericError)\s\d{1}\s([a-z0-9]{16}):\d{1}\b)|(Err:)')
        for region in regions:
            for line in v.lines(region):
                s = v.substr(line)
                resultStr = resultStr + s + '\n'
        if resultStr:
            newView = v.window().new_file()
            newView.run_command("insert", {"characters": resultStr})
            newView.run_command("insert", {"characters": "Execute time: " + str((datetime.datetime.now() - startTime).seconds) + " Sec"})
            #newView.show_popup("Execute time: " + str((datetime.datetime.now() - startTime).seconds) + " Sec", sublime.HTML, location=-1, on_navigate=print)
            newView.set_syntax_file('Packages/User/SiebelLog.tmLanguage')
        sublime.status_message("Complete - ShowOnlyErrorCommand")
        