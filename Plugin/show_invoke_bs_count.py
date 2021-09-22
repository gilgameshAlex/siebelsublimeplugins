#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import sublime
import sublime_plugin
import re
import datetime


class ShowInvokeBsCountCommand(sublime_plugin.WindowCommand):
    def run(self):
        v = self.window.active_view()
        resultStr = ""
        startTime = datetime.datetime.now()
        myDict = {}
        regions = v.find_all(r'Begin: Business Service')#, sublime.IGNORECASE,"\2:")
        for region in regions:
            for line in v.lines(region):
                s = v.substr(line)
                str2 = re.findall(r'\'[\(\)\#\d\s\w]+\'', s)
                svcItem = "BS: " + str2[0] + " METHOD: " + str2[1]

                if svcItem in myDict:
                    myDict[svcItem] = myDict[svcItem] + 1
                else:
                    myDict[svcItem] = 1

        sortedDict = {}
        sortedKeys = sorted(myDict, key=myDict.get)
        for w in sortedKeys:
            sortedDict[w] = myDict[w]
        for i in sortedDict.keys():
            resultStr = resultStr + i + "    COUNT = " + str(sortedDict[i]) + "\n"
        if resultStr:
            newView = v.window().new_file()
            newView.run_command("insert",{"characters": resultStr})
            newView.run_command("insert",{"characters": "Execute time: " + str((datetime.datetime.now() - startTime).seconds) + " seconds"})
            #newView.show_popup(, sublime.HTML, location=-1, on_navigate=print)
            newView.set_syntax_file('Packages/User/SiebelLog.tmLanguage')
        sublime.status_message("Complete - ShowInvokeBsCountCommand")
