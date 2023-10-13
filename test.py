def print_tree(tree, indent=''):
    length = len(tree)
    for index, (key, value) in enumerate(tree.items()):
        if isinstance(value, dict):
            if index == length - 1:
                print(f'{indent}└── {key}')
                print_tree(value, indent + '    ')
            else:
                print(f'{indent}├── {key}')
                print_tree(value, indent + '│   ')
        else:
            if index == length - 1:
                print(f'{indent}└── {key}: {value}')
            else:
                print(f'{indent}├── {key}: {value}')

tree = {
    'root': {
        'node1': {
            'leaf1': '1',
            'leaf2': '2'
        },
        'node2': {
            'leaf3': '3',
            'leaf4': '4'
        }
    },
    'root2': {
        'node1': {
            'leaf1': '1',
            'leaf2': '2'
        },
        'node2': {
            'leaf3': '3',
            'leaf4': '4'
        }
    }
}

print_tree(tree)
