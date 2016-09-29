import os
from jinja2 import Environment, FileSystemLoader


def render(tpl, output_path, **kwargs):

    node = {
        'class_name': "test3",
        "mtype_id":   "0x1A005",
        "input_ports": [
            {
                "name": "aa",
                "type": "Mat44",
                "affects": [
                    "ao"
                ]
            },
            {
                "name": "bb",
                "type": "Mat44",
                "affects": [
                    "oo"
                ]
            }
        ],
        "output_ports": [
            {
                "name": "ao",
                "type": "Mat44"
            },
            {
                "name": "oo",
                "type": "Mat44"
            }
        ]
    }

    canvas_file_path = r"D:\\fabric\\hogea.canvas"

    results = tpl.render(node=node, canvas_file_path=canvas_file_path)

    with open(output_path, 'w') as f:
        f.write(results)

    return results


if __name__ == '__main__':
    cwd = os.path.abspath(os.path.dirname(__file__))
    template_dir = cwd
    # template_dir = os.path.join(cwd, 'node.cpp.tpl')

    env = Environment(loader=FileSystemLoader(template_dir, encoding='utf8'))
    cpp_tpl = env.get_template('node.tpl.cpp')
    render(cpp_tpl, "test3.cpp")

    cpp_tpl = env.get_template('node.tpl.h')
    render(cpp_tpl, "test3.h")
