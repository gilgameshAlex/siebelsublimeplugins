#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import sublime
import sublime_plugin
import re
import datetime


class ShowExecTimeWfCommand(sublime_plugin.WindowCommand):
    def run(self):
        v = self.window.active_view()

        level = 0
        resultStr = ""
        startTime = datetime.datetime.now()
        regions = v.find_all(r'(Реализация определения процесса)|(Реализация определения шага)|(Остановка экземпляра шага)|(Остановка экземпляра процесса)|(Instantiating step definition)|(Stopping step instance of)|(Instantiating process definition)|(Stopping process instance of)')#, sublime.IGNORECASE,"\2:")
        for region in regions:
            for line in v.lines(region):
                s = v.substr(line)
                s = s.replace('(', '')
                s = s.replace(')', '')
                s = s.replace('.', '')
                print (s)
                match = re.search('(Реализация определения процесса)|(Instantiating process definition)', s)
                if match:
                    level = level + 1
                    str2 = re.findall (r'\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,2}', s)
                    t1 = datetime.datetime.strptime(str2[0], "%Y-%m-%d %H:%M:%S")
                    s = re.sub (r'.+Реализация определения процесса\s+', '', s)
                    s = re.sub (r'.+Instantiating process definition\s+', '', s)
                    resultStr = resultStr + "[START WF] " + s + " [" + str(t1) + ']\n'
                else:
                    match = re.search('(Реализация определения шага)|(Instantiating step definition)', s)
                    if match:
                        str2 = re.findall (r'\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,2}', s)
                        t1 = datetime.datetime.strptime(str2[0], "%Y-%m-%d %H:%M:%S")
                        s = re.sub (r'.+Реализация определения шага\s+', '', s)
                        s = re.sub (r'.+Instantiating step definition\s+', '', s)

                        #i = 0
                        #while i < (level * 4):
                        #    resultStr = resultStr + " "
                        #    i = i + 1
                        #for k in range (1):
                        #    resultStr = resultStr + ' '
                        resultStr = resultStr + str(level) +"-[STEP] " + s
                    else:
                        match = re.search('(Остановка экземпляра шага)|(Stopping step instance of)', s)
                        if match:
                            str2 = re.findall (r'\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,2}', s)
                            t2 = datetime.datetime.strptime(str2[0], "%Y-%m-%d %H:%M:%S")
                            resultStr = resultStr + " [" + str((t2-t1).seconds) +' sec]\n'
                        else:
                            match = re.search(r'(Остановка экземпляра процесса)|(Stopping process instance of)', s)
                            if match:
                                level = level - 1
                                str2 = re.findall (r'\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,2}', s)
                                t1 = datetime.datetime.strptime(str2[0], "%Y-%m-%d %H:%M:%S")
                                s = re.sub (r'.+Остановка экземпляра процесса\s+', '', s)
                                s = re.sub (r'.+Stopping process instance of\s+', '', s)
                                resultStr = resultStr + "[END WF] " + s + " [" + str(t1) + ']\n';
        if resultStr:
            newView = v.window().new_file()
            newView.run_command("insert",{"characters": resultStr})
            newView.run_command("insert",{"characters": "Execute time: " + str((datetime.datetime.now() - startTime).seconds) + " seconds"})
            #newView.show_popup(, sublime.HTML, location=-1, on_navigate=print)
            newView.set_syntax_file('Packages/User/SiebelLog.tmLanguage')
        sublime.status_message("Complete - ShowExecTimeWfCommand")