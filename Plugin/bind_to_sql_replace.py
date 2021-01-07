#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import sublime
import sublime_plugin
import re
import datetime


class BindToSqlReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        v = self.view
        startTime = datetime.datetime.now()
        regions = v.sel()
        sql_query = ""

        for region in regions:
            sql_query = sql_query + v.substr(region)
            lines = v.lines(region)
            for line in lines:
                s = v.substr(line)
                index_find = s.find("Bind variable ")
                if index_find != -1:
                    split_str = s.partition("Bind variable ")
                    split_data = split_str[2].partition(": ")
                    sql_query = re.sub(r":" + str(split_data[0]) + r"\b", "'" + split_data[2] + "'", sql_query)
                else:
                    sql_query = sql_query + s
        
        index_log = sql_query.find('ObjMgrSqlLog')
        if index_log != -1:
            sql_query = sql_query[:index_log]

        index_log = sql_query.find('SQLParseAndExecute')
        if index_log != -1:
            sql_query = sql_query[:index_log]

        self.view.replace(edit, region, sql_query)
        #if sql_query:
        #    newView = v.window().new_file()
            #newView.run_command("append",{"characters": sql_query})
            #newView.run_command("append",{"characters": "\nExecute time: " + str((datetime.datetime.now() - startTime).seconds) + " seconds"})
        #    newView.settings().set('auto_indent', False)
        #    newView.run_command("insert",{"characters": sql_query})
            #newView.run_command("insert",{"characters": "\nExecute time: " + str((datetime.datetime.now() - startTime).seconds) + " seconds"})
        #    newView.settings().erase('auto_indent')
        #    newView.set_syntax_file('Packages/User/SiebelLog.tmLanguage')
        sublime.status_message("Complete - BindToSqlReplaceCommand")