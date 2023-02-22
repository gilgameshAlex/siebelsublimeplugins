#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import sublime
import sublime_plugin
import re
import datetime


class ShowExecTimeSqlCommand(sublime_plugin.WindowCommand):
    def run(self):
        v = self.window.active_view()

        level = 0
        resultStr = ""
        startTime = datetime.datetime.now()
        myDict = {}
        regions = v.find_all(r'SQL Statement Execute Time for SQL Cursor with ID')#, sublime.IGNORECASE,"\2:")
        #regions = v.find_all(r'(Реализация определения процесса)|(Реализация определения шага)|(Остановка экземпляра шага)|(Остановка экземпляра процесса)|(Instantiating step definition)|(Stopping step instance of)|(Instantiating process definition)|(Stopping process instance of)')#, sublime.IGNORECASE,"\2:")
        
        for region in regions:
            for line in v.lines(region):
                s = v.substr(line)
                str2 = re.findall(r'ID.+:', s)
                svcItem = "Cursor: " + str2[0]
                str4 = re.sub(r'ID.+:','',s)
                str3 = re.findall(r'\s[\d\.]+', str4);
                myDict[svcItem] = str3[0]
        sortedDict = {}
        sortedKeys = sorted(myDict, key=myDict.get)
        for w in sortedKeys:
            sortedDict[w] = myDict[w]
        for i in sortedDict.keys():
            resultStr = resultStr + i + "    TIME = " + str(sortedDict[i]) + " sec\n"
        if resultStr:
            newView = v.window().new_file()
            newView.run_command("insert",{"characters": resultStr})
            newView.run_command("insert",{"characters": "Execute time: " + str((datetime.datetime.now() - startTime).seconds) + " seconds"})
            #newView.show_popup(, sublime.HTML, location=-1, on_navigate=print)
            newView.set_syntax_file('Packages/User/SiebelLog.tmLanguage')
        sublime.status_message("Complete - ShowExecTimeSqlCommand")
