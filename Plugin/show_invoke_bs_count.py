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
        arrSvcName = ['']
        arrSvcCount = [0]
        regions = v.find_all(r'Begin: Business Service')#, sublime.IGNORECASE,"\2:")
        for region in regions:
            for line in v.lines(region):
                s = v.substr(line)
                str2 = re.findall(r'\'[\(\)\#\d\s\w]+\'', s)
                svcItem = "BS: " + str2[0] + " METHOD: " + str2[1]

                if svcItem in arrSvcName:
                    index = arrSvcName.index(svcItem)
                    arrSvcCount[index] = arrSvcCount[index] + 1
                else:
                    arrSvcName.append(svcItem)
                    index = arrSvcName.index(svcItem)
                    arrSvcCount.insert(index, 1)

        for i in arrSvcName:
            resultStr = resultStr + str(i) + "    COUNT = " + str(arrSvcCount[arrSvcName.index(i)]) + "\n"
        if resultStr:
            newView = v.window().new_file()
            newView.run_command("insert",{"characters": resultStr})
            newView.run_command("insert",{"characters": "Execute time: " + str((datetime.datetime.now() - startTime).seconds) + " seconds"})
            #newView.show_popup(, sublime.HTML, location=-1, on_navigate=print)
            newView.set_syntax_file('Packages/User/SiebelLog.tmLanguage')
        sublime.status_message("Complete - ShowInvokeBsCountCommand")
