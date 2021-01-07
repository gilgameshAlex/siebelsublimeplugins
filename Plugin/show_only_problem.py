import sublime
import sublime_plugin
import re
import datetime

class ShowOnlyProblemCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        v = self.view
        resultStr = ""
        startTime = datetime.datetime.now()
        for region in v.find_all(r'Warning\s+\d{1}\s+([a-z0-9]{16}):\d{1}'):
            for line in v.lines(region):

                s = v.substr(line)
                resultStr = resultStr + s + '\n';
        if resultStr:
            newView = v.window().new_file()
            newView.run_command("insert",{"characters":"PreExecute time: " + str((datetime.datetime.now() - startTime).seconds) + " MSec"})
            newView.run_command("insert",{"characters": resultStr + '\n'})
            newView.run_command("insert",{"characters":"Execute time: " + str((datetime.datetime.now() - startTime).seconds) + " MSec"})
            newView.set_syntax_file('Packages/User/SiebelLog.tmLanguage') 
        sublime.status_message("Complete - ShowOnlyProblemCommand")