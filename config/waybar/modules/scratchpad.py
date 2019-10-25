#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from i3ipc import Connection

i3 = Connection()

con = i3.get_tree()

scratchpad = con.find_named('__i3_scratch') if con.find_named('__i3_scratch') else []
leaves = scratchpad[0].floating_nodes
num_leaves = len(scratchpad[0].floating_nodes)
output = '{"text":" %s"}' % num_leaves if num_leaves > 0 else '{"text":""}'
print(output)
