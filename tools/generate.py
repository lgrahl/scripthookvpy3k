"""
Parse natives.h, generate wrapper with SWIG and apply namespaces in
the generated wrapper.
"""
import os
import subprocess
import io

from distutils.version import StrictVersion
import sys

path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
natives_h = os.path.join(path, 'sdk', 'inc', 'natives.h')
natives_i = os.path.join(path, 'cpp', 'src', 'natives.i')
gta_native_py_in = os.path.join(path, 'cpp', 'src', 'gta_native.py')
gta_native_py_out = os.path.join(path, 'python', 'gta_native.py')

swig_path = os.path.join(path, 'swig')
swig_version = ['swig', '-version']
swig_generate = ['swig', '-python', '-c++', natives_i]
swig_required_version = '3.0.5'


def main():
    # Change to SWIG path
    os.chdir(swig_path)

    # Check SWIG version
    for line in io.StringIO(subprocess.check_output(swig_version).decode('utf-8')):
        if line.startswith('SWIG Version '):
            *init, version = line.split('SWIG Version ')
            version = StrictVersion(version.strip())
            if version >= StrictVersion(swig_required_version):
                print('SWIG Version:', version)
                break
    else:
        fail('SWIG Version >= {} required'.format(swig_required_version), 2)

    # Map namespaces to function names
    date = 'Unknown'
    functions = {}
    namespace = 'default'
    print('Mapping namespaces to functions')
    with open(natives_h) as natives:
        for line in natives:
            line = line.strip()

            # Date
            if line.startswith('// Generated'):
                _, date_ = line.split('// Generated')
                date = date_.strip()

            # Namespace
            if line.startswith('namespace'):
                head, namespace, *tail = line.split(' ')
                namespace = namespace.lower()

            # Function
            if line.startswith('static'):
                *init, last = line.split(' ', maxsplit=2)
                name, *tail = last.split('(', maxsplit=1)
                functions.setdefault(namespace, set())
                functions[namespace].add(name)

    # Generate wrapper
    print('Generating wrapper')
    try:
        subprocess.check_call(swig_generate)
    except subprocess.CalledProcessError as exc:
        fail(exc, 3)

    # Rewrite Python wrapper
    last_namespace = None
    function_found = False
    skip = 0
    indent = ' ' * 4
    init = []
    middle = ["__version__ = '{}'\n\n\n".format(date.strip("'"))]
    tail = []

    def add_normal(_line):
        if function_found:
            tail.append(_line)
        else:
            init.append(_line)

    def add_class_assignment():
        if last_namespace is not None:
            middle.append('{} = _{}\n\n\n'.format(
                last_namespace, last_namespace.capitalize()))

    def maybe_add_method(_line):
        nonlocal last_namespace, function_found
        for _namespace, names in functions.items():
            for _name in names:
                if _line.startswith('def {}('.format(_name)):
                    function_found = True
                    if _namespace != last_namespace:
                        # Insert class assignment at the end of a namespace
                        add_class_assignment()

                        # Insert class declaration at the start of a namespace
                        middle.append('class _{}(_object):\n'.format(_namespace.capitalize()))
                        last_namespace = _namespace

                    # Insert staticmethod and function definition
                    *_, _last = _line.split('(', maxsplit=1)
                    middle.append(indent + '@staticmethod\n')
                    middle.append(indent + 'def {}({}'.format(
                        _name if _name.startswith('_') else _name.lower(),
                        _last
                    ))
                    return 3
        add_normal(_line)
        return 0

    # Parse generated Python wrapper
    print('Parsing generated Python wrapper')
    with open(gta_native_py_in) as natives_in:
        for line in natives_in:
            if skip > 0:
                # Return statement
                if skip == 3:
                    middle.append('{}{}\n'.format(indent, line))
                elif skip == 1 and len(line.strip()) > 0:
                    add_normal(line)
                skip -= 1
            elif line.startswith('def '):
                # Function
                skip = maybe_add_method(line)
            else:
                # Something else
                add_normal(line)
        add_class_assignment()

    # Write new Python wrapper
    print('Writing new Python wrapper')
    with open(gta_native_py_out, 'w') as natives_out:
        natives_out.writelines(init + middle + tail)

    # Remove originally generated Python wrapper
    print('Removing originally generated Python wrapper')
    os.remove(gta_native_py_in)

    # Done
    print('Done')
    sys.exit(0)


def fail(message, status):
    print(message, file=sys.stderr)
    sys.exit(status)

if __name__ == '__main__':
    main()
