import jinja2
templateLoader = jinja2.FileSystemLoader( searchpath="." )
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "tpl.jinja"
template = templateEnv.get_template( TEMPLATE_FILE )
templateVars = { "title" : "Test Example",
                 "description" : "A simple inquiry of function." }
outputText = template.render( templateVars )
print(outputText)


# import re
#
# s = """aaa@xxx.com bbb@yyy.net
#
# {{{
#   a = b
#   c = d
# }}}
#  ccc@zzz.org
# """
#
# res = re.findall("({{{.*}}})", s, flags=re.DOTALL)
# print(res)
#
# print(re.sub('{{{(.*)}}}', '\\1', s, flags=re.DOTALL))
# #.replace("\n", " ")
# # xxx@aaa.com yyy@bbb.net zzz@ccc.org
#
#
# def convert_case(match_obj):
#     return match_obj.group(2).replace("\n", " ")
#
# print("-----------------------")
# print(re.sub("({{{)(.*)(}}})", convert_case, s, flags=re.DOTALL))
