# from bs4 import BeautifulSoup
# import requests
# from manager.config import TASKS_URL, LOGIN_URL, HEADERS, DATA
# import json
# import re
# # from slimit import ast
# # from slimit.parser import Parser
# # from slimit.visitors import nodevisitor
#
#
# def parse():
#     session = login()
#     html = get_html(session, TASKS_URL)
#     if html.status_code == 200:
#         return get_content(html.text)
#     else:
#         print("Error")
#
#
# def login():
#     session = requests.Session()
#     session.post(LOGIN_URL, data=DATA, headers=HEADERS)
#     return session
#
#
# def get_html(session, url, params=None):
#     r = session.get(url, headers=HEADERS, params=params)
#     return r
#
#
# def get_content(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     scripts = soup.find_all('script')
#     # for script in scripts:
#     #     data = script.contents[0]
#     #     parser = Parser()
#     #     tree = parser.parse(data)
#     #     fields = {getattr(node.left, 'value', ''): getattr(node.right, 'value', '')
#     #               for node in nodevisitor.visit(tree)
#     #               if isinstance(node, ast.Assign)}
#     return 1
# parse()
