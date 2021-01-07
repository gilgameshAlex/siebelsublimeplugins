import sublime
import sublime_plugin
import re


class TestCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        v = self.view
        newView = v.window().new_file()
        newView.set_syntax_file('Packages/User/SiebelLog.tmLanguage')
        newView.run_command("insert",{"characters": "1"})
        newView.run_command("insert",{"characters": "\n2"})
        