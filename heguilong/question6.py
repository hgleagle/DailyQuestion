#!/usr/bin/env python3
"""
File: question6.py
Author: heguilong
Email: hgleagle@gmail.com
Github: https://github.com/hgleagle

今天来第六题，设计一个程序，用于统计一个项目中的代码数，包括文件个数，代码行数，注释行数，空行行数

尽量设计灵活一点可以通过输入不同参数来统计不同语言的项目

例如：python counter.py --lang python  用于统计python代码，lang是java就用于统计java代码

输出：

files:10
code_lines:200
comments:100
blanks:20
"""
import os
#  import sys
import logging
import fire


prog_lang_dict = {
    "python": {"ext": ["py"], "single": "#", "start_comment": ["'''", '"""'], "end_comment": ["'''", '"""']},
    "java": {"ext": ["java"], "single": "//", "start_comment": ["/*"], "end_comment": ["*/"]},
    "C": {"ext": ["c", "h"], "single": "//", "start_comment": ["/*"], "end_comment": ["*/"]},
    "C++": {"ext": ["cpp", "h"], "single": "//", "start_comment": ["/*"], "end_comment": ["*/"]}
}

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Project():
    """
    count code lines in the project
    """
    def __init__(self, path, lang):
        """TODO: Docstring for __init__.

        :path: TODO
        :returns: TODO

        """
        self.files = 0
        self.code_lines = 0
        self.comments = 0
        self.blanks = 0
        self.path = path
        self.file_types = prog_lang_dict[lang]['ext']
        self.single_comment_sign = prog_lang_dict[lang]['single']
        self.multi_start_comment_sign = prog_lang_dict[lang]['start_comment']
        self.multi_end_comment_sign = prog_lang_dict[lang]['end_comment']

    def parse(self, filename):
        in_multi_comment = False
        self.files += 1
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()

                con1 = con2 = con3 = False
                for index, start_comment in enumerate(self.multi_start_comment_sign):
                    if line.startswith(start_comment) and line.endswith(self.multi_end_comment_sign[index]) \
                            and len(line) > len(start_comment):
                        con1 = True
                        break

                for item in self.multi_end_comment_sign:
                    if line.startswith(item):
                        con2 = True
                        break

                # 多行注释分布多行，开始行，结束行
                for item in self.multi_start_comment_sign + self.multi_end_comment_sign:
                    if line.startswith(item):
                        con3 = True
                        break

                # 不在多行注释内的空行统计
                if line == '' and not in_multi_comment:
                    self.blanks += 1
                    logging.debug("file %s, line %s, blank" % (filename, line))
                # 单行注释
                # 多行注释在一行
                # 多行注释中间行
                elif line.startswith(self.single_comment_sign) or con1 or (in_multi_comment and not con2):
                    self.comments += 1
                    logging.debug("file %s, line %s comment" % (filename, line))
                elif con3:
                    self.comments += 1
                    in_multi_comment = not in_multi_comment
                    logging.debug("file %s, line %s, comment in mutliline" % (filename, line))
                else:
                    self.code_lines += 1
                    logging.debug("file %s, line %s, codeline" % (filename, line))

    def count(self):
        """count files, blanks, code_lines, comments in the project """
        self.files = self.code_lines = self.comments = self.blanks = 0
        for foldername, subfolders, filenames in os.walk(self.path):
            for filename in filenames:
                for filetype in self.file_types:
                    if filename.endswith(filetype):
                        self.parse(filename)
        return self  # for fire chaining function call

    def __str__(self):
        return "file: %d\ncode_lines: %d\ncomments: %d\nblanks: %d" % (
            self.files, self.code_lines, self.comments, self.blanks)


if __name__ == "__main__":
    # solution 1
    # if len(sys.argv) != 3:
        # print("Usage: python3 question6.py --lang [language]")
        # sys.exit()
    # elif sys.argv[1] != '--lang':
        # print("should start with --")
        # sys.exit()
    # elif sys.argv[2] not in prog_lang_dict:
        # print("language can be python, C, C++, java")
        # sys.exit()

    # project = Project(os.getcwd(), sys.argv[2])
    # project.count()
    # print(project)

    # solution 2: use fire library
    # Usage: python3 question6.py --path=. --lang=python count __str__
    fire.Fire(Project)
