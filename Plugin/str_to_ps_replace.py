#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import sublime
import sublime_plugin
import re
import datetime

class StrToPsReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        v = self.view
        resultStr = ""
        startTime = datetime.datetime.now()
        regions = v.sel()
        for region in regions:
            s = v.substr(region)
            list_res = s.split("*")
            size_res = len(list_res)
            cur_index = 7
            st_value  = int(list_res[cur_index - 1])
            resultStr, cur_index, st_value = StrToPsReplaceCommand.TravelTree(0, 0, st_value, list_res, size_res, size_res, cur_index, resultStr)
            self.view.replace(edit, region, resultStr)
        sublime.status_message("Complete - StrToPsReplace")

    def TravelTree(level, limit, nextLen, list_res, list_size, list_limit_size, start_index, result_str):
        cur_index = start_index
        st_value  = nextLen
        resultStr = result_str
        begin  = True
        first_run = True
        local_limit = limit
        cur_limit = 0
        while True:
            if cur_index > list_limit_size or  cur_index >= list_size or (local_limit > 0 and cur_limit >= local_limit):
                return [resultStr, cur_index - 1, st_value]
            else:
                cur_str = list_res[cur_index]
                if begin:
                    if cur_str.isdigit():
                        next_level = level + 1
                        next_lenght = int(list_res[cur_index + 1])
                        next_position = cur_index + 2
                        next_size = next_position + st_value * 2 + int(cur_str) + 1
                        if int(cur_str) == 0:
                            resultStr, cur_index, st_value = StrToPsReplaceCommand.TravelTree(next_level, 0, next_lenght, list_res, list_size, next_size, next_position, resultStr)
                        else:
                            resultStr, cur_index, st_value = StrToPsReplaceCommand.TravelTree(next_level, int(cur_str), next_lenght, list_res, list_size, list_size, next_position, resultStr)
                        cur_limit = cur_limit + 1
                    else:
                        begin = False
                        i = 0
                        if first_run:
                            lvl_tmp = level - 1
                            first_run = False
                        else:
                            lvl_tmp = level

                        while i < lvl_tmp:
                            resultStr = resultStr + "-"
                            i = i + 1

                        resultStr = resultStr + "[" + cur_str[:st_value] + "]"
                        st_value = int(cur_str[st_value:])
                else:
                    begin = True
                    if st_value > 0:
                        resultStr = resultStr + "='" + cur_str[:st_value] +"'\n"
                    else:
                        resultStr = resultStr + "\n"
                    if cur_index + 1 < list_size:
                        st_value = int(cur_str[st_value:])
            cur_index = cur_index + 1
