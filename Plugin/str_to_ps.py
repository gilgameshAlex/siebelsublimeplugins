#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import sublime
import sublime_plugin
import re
import datetime

class StrToPs(sublime_plugin.TextCommand):
    def run(self, edit):
        print("___________NEW RUN___________")
        v = self.view
        resultStr = ""
        startTime = datetime.datetime.now()
        regions = v.sel()
        begin  = True
        level = 0
        need_skip = False
        print("PreFOR")
        for region in regions:
            s = v.substr(region)
            #ps = s[15:]
            list_res = s.split("*")
            j = 0
            for str_p in list_res:
                print(str(j)+"-"+str_p)
                j=j+1
            size_res = len(list_res)
            limit = int(list_res[3])
            cur_index = 7
            st_value  = int(list_res[cur_index - 1])
            print("PreInvoke TravelTree")
            resultStr, cur_index = StrToPs.TravelTree(level, 0, st_value, list_res, size_res, size_res, cur_index, resultStr)
            
        if resultStr:
            newView = v.window().new_file()
            newView.run_command("append",{"characters": resultStr})
            newView.run_command("append",{"characters": "\nExecute time: " + str((datetime.datetime.now() - startTime).seconds) + " seconds"})
            #newView.show_popup(, sublime.HTML, location=-1, on_navigate=print)
            newView.set_syntax_file('Packages/User/SiebelLog.tmLanguage')
        sublime.status_message("Complete - StrToPS")

    def TravelTree(level, limit, nextLen, list_res, list_size, list_limit_size, start_index, result_str):
        print("_____________________InvokeTravelTree")
        cur_index = start_index
        print("cur_index="+str(cur_index))
        st_value  = nextLen
        print("st_value="+str(st_value))
        resultStr = result_str
        print("resultStr="+str(resultStr))

        begin  = True
        first_run = True
        local_limit = limit
        print("local_limit="+str(local_limit))
        cur_limit = 0
        while True:
            if cur_index > list_limit_size or  cur_index >= list_size or (local_limit > 0 and cur_limit >= local_limit):
                print("c="+str(cur_index)+" l="+str(list_size)+" ll="+str(list_limit_size))
                print("local_limit="+str(local_limit)+" cur_limit="+str(cur_limit))
                return [resultStr, cur_index - 1]
            else:
                print("cur_index="+str(cur_index))
                print("st_value="+str(st_value))
                cur_str = list_res[cur_index]
                print("cur_str="+cur_str)
                if begin:
                    if cur_str.isdigit():
                        print("resultStrPRETRAVEL="+resultStr)
                        print("cur_index="+str(cur_index))
                        print("level="+str(level))
                        print("list_size="+str(list_size))
                        print("list_limit_size="+str(list_limit_size))
                        print("list_res[cur_index]="+list_res[cur_index])
                        print("st_value="+str(st_value))
                        next_level = level + 1
                        next_lenght = int(list_res[cur_index + 1])
                        next_position = cur_index + 2
                        next_size = next_position + st_value * 2 + int(cur_str) + 1
                        print("next_position="+str(next_position))
                        print("next_lenght="+str(next_lenght))
                        #cur_index = cur_index + 2
                        #resultStr, cur_index = StrToPs.TravelTree(next_level, next_lenght, list_res, next_size, next_position, resultStr)
                        if int(cur_str) == 0:
                            resultStr, cur_index = StrToPs.TravelTree(next_level, 0, next_lenght, list_res, list_size, next_size, next_position, resultStr)
                        else:
                            resultStr, cur_index = StrToPs.TravelTree(next_level, int(cur_str), next_lenght, list_res, list_size, list_size, next_position, resultStr)
                        cur_limit = cur_limit + 1
                        #return [resultStr, cur_index]
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
                        #print("bName="+cur_str)
                        #print("bSize="+cur_str[st_value:])
                        st_value = int(cur_str[st_value:])
                else:
                    begin = True
                    #print(cur_str)
                    #print(cur_str[:st_value])
                    #print(cur_str[st_value:])
                    if st_value > 0:
                        resultStr = resultStr + "='" + cur_str[:st_value] +"'\n"
                    else:
                        resultStr = resultStr + "\n"
                    #print("st="+str(st_value) +" len="+str(len(cur_str)))
                    #if st_value < len(cur_str):
                    if cur_index <= list_size:
                        st_value = int(cur_str[st_value:])
            cur_index = cur_index + 1





            #print (str(list_res[7])[:int(st_value)])
            #while cur_index < size_res:
            #    cur_str = list_res[cur_index]
            #    if begin:
            #        if cur_str.isdigit():
            #            cur_index = cur_index + 1
            #            level = level + 1
            #            cur_str = list_res[cur_index]
            #            st_value = int(cur_str)
            #        else:
            #            begin = False
            #            i = 0
            #            while i < level:
            #                resultStr = resultStr + "-"
            #                i = i + 1
            #            resultStr = resultStr + "[" + cur_str[:st_value] + "]"
            #            print("bName="+cur_str)
            #            print("bSize="+cur_str[st_value:])
            #            st_value = int(cur_str[st_value:])
            #    else:
            #        begin = True
                    #print(cur_str)
                    #print(cur_str[:st_value])
                    #print(cur_str[st_value:])
            #        resultStr = resultStr + "='" + cur_str[:st_value] +"'\n"
                    #print("st="+str(st_value) +" len="+str(len(cur_str)))
            #        if st_value < len(cur_str):
            #            st_value = int(cur_str[st_value:])
            #    cur_index = cur_index + 1


            ##k = 1
            ##for res in list_res:
            ##    if len(res) > 1 or (len(res) == 1 and k == size_res):
            ##        if not need_skip:
            ##            if begin:
                            ##Если ==1, значить проперти
            ##                if int(res[-1:]) != 0:
            ##                    i = 0
            ##                    while i < level:
                                    #resultStr = resultStr + "-"
            ##                        i = i + 1
                                #resultStr = resultStr + res[:-1]
            ##                    begin = False
                            ##Иначе дочерний элемент
            ##                else:
            ##                    level = level + 1
            ##                    i = 0
            ##                    while i < level:
            ##                        resultStr = resultStr + "-"
            ##                        i = i + 1
                                #resultStr = resultStr + res[:-1] + "\n"
            ##                    need_skip = True
                        #else:
                            ##Если последний элемент, то не обрезаем последний символ
                            #if k == size_res:
                                #resultStr = resultStr + "=" + res + "\n"
                            ##Обрезаем последний символ элемента
                            #else:
                                #resultStr = resultStr + "=" + res[:-1] + "\n"
                            #    begin = True
                    #else:
                    #    need_skip = False
                #else:
                #    print(res)
                #    need_skip = False
                #    begin = True
                #k = k + 1