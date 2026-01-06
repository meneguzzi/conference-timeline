#!/usr/bin/env ruby
# -----------------------------------------------
# Timeline
# -----------------------------------------------
# Felipe Meneguzzi, based on Mau's ruby
# -----------------------------------------------
import re
import sys

if len(sys.argv) > 1 and sys.argv[1] == '-h':
    print('python timeline.py [filename=README.md] [dir=LR]')
else:
    # Arguments
    filename = sys.argv[1] if len(sys.argv) > 1 else 'README.md'
    dir = sys.argv[2] if len(sys.argv) > 2 else 'LR'

    # Setup
    nodes = {}
    url = {}
    node_counter = cluster_counter = 0
    output = f'digraph timeline {{\n  rankdir={dir}\n  nodesep=0.15\n  node [target=_blank]\n\n'

    # Generate graph based on filename lines starting with "## month" and "- conferenceName description"
    timeline = False

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('# Conference Timeline'):
                timeline = True

            if timeline:
                if re.match(r'- \[(.+)\](.*)$', line):  #line.startswith('- ['):
                    match = re.match(r'- \[(.+)\](.*)$', line)
                    if match:
                        node_name = match.group(1)
                        node_description = match.group(2).strip()
                        if node_name in nodes:
                            nodes[node_name].append([f'node_{node_counter}'])
                        else:
                            nodes[node_name] = [f'node_{node_counter}']

                        output += f'    node_{node_counter} [shape=box label="{node_name}\\n{node_description}"{url.get(node_name, "")}]\n'
                        node_counter += 1
                elif re.match(r'##\s+(.*)$', line):  # line.startswith('## '):
                    # cluster_name = line[3:].strip()
                    match = re.match(r'##\s+(.*)$', line)
                    if match:
                        cluster_name = match.group(1)
                        if cluster_counter != 0:
                            output += '  }\n\n'
                        output += f'  subgraph cluster_{cluster_counter} {{\n    label="{cluster_name}"\n    order_node_{cluster_counter} [shape=point height=0 style=invis]\n'
                        cluster_counter += 1
                elif re.match(r'^\[(.+)\]:\s+(\S+)(\s+("[^"]+"))?$', line):
                    match = re.match(r'^\[(.+)\]:\s+(\S+)(\s+("[^"]+"))?$', line)
                    if match:
                        link_name = match.group(1)
                        link_url = match.group(2)
                        link_tooltip = match.group(4) or ""
                        url[link_name] = f' URL="{link_url}" tooltip={link_tooltip}'

    # Close last cluster
    if cluster_counter != 0:
        output += '  }\n'

    # Add edges between nodes
    for parts in nodes.values():
        output += '\n  '
        if len(parts) > 1:
            output += parts + ' -> '

    # Add invisible edges between clusters to enforce order
    output += '\n'
    for i in range(cluster_counter - 1):
        output += f'\n  order_node_{i} -> order_node_{i + 1} [style=invis]'

    output += '\n}'

    # Save file
    with open(f'{filename}.dot', 'w') as output_file:
        output_file.write(output)