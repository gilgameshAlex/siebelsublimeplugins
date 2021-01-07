import sublime
import sublime_plugin
import re
import datetime


class ShowOnlyProblemAsyncCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        source_view = self.view
        new_view = source_view.window().new_file()
        #new_view.set_syntax_file('Packages/User/SiebelLog.tmLanguage') 

        def cb():
            self.filter(source_view, new_view)
        sublime.set_timeout_async(cb, 0)

    def filter (self, source_view, output_view):
        resultStr = ""
        startTime = datetime.datetime.now()
        regions = source_view.find_all(r'Warning\s+\d{1}\s+([a-z0-9]{16}):\d{1}')
        for region in regions:
            for line in source_view.lines(region):
                s = source_view.substr(line)
                output_view.run_command('test_append', {'text': s+'\n'})

class TestAppendCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        self.view.insert(edit, self.view.size(), text)