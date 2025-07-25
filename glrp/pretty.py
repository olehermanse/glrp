# Taken from cfbs and simplified:
# https://github.com/cfengine/cfbs/blob/master/cfbs/pretty.py

# MIT License

# Copyright (c) 2021 Northern.tech

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
from collections import OrderedDict


def pretty_check_file(filename):
    with open(filename) as f:
        s = f.read()
    o = json.loads(s, object_pairs_hook=OrderedDict)
    return s == pretty(o) + "\n"


def pretty_check_string(s):
    o = json.loads(s, object_pairs_hook=OrderedDict)
    return s == pretty(o)


def pretty_file(filename):
    with open(filename) as f:
        old_data = f.read()
    new_data = pretty_string(old_data) + "\n"
    if old_data != new_data:
        with open(filename, "w") as f:
            f.write(new_data)
        return True
    return False


def pretty_string(s):
    s = json.loads(s, object_pairs_hook=OrderedDict)
    return pretty(s)


def pretty(o):
    MAX_LEN = 80
    INDENT_SIZE = 2

    def _should_wrap(parent, indent):
        assert isinstance(parent, (tuple, list, dict))
        # We should wrap the top level collection
        if indent == 0:
            return True
        if isinstance(parent, dict):
            parent = parent.values()

        count = 0
        for child in parent:
            if isinstance(child, (tuple, list, dict)):
                if len(child) >= 2:
                    count += 1
        return count >= 2

    def _encode_list(lst, indent, cursor):
        if not lst:
            return "[]"
        if not _should_wrap(lst, indent):
            buf = json.dumps(lst)
            assert "\n" not in buf
            if indent + cursor + len(buf) <= MAX_LEN:
                return buf

        indent += INDENT_SIZE
        buf = "[\n" + " " * indent
        first = True
        for value in lst:
            if first:
                first = False
            else:
                buf += ",\n" + " " * indent
            buf += _encode(value, indent, 0)
        indent -= INDENT_SIZE
        buf += "\n" + " " * indent + "]"

        return buf

    def _encode_dict(dct, indent, cursor):
        if not dct:
            return "{}"
        if not _should_wrap(dct, indent):
            buf = json.dumps(dct)
            buf = "{ " + buf[1 : len(buf) - 1] + " }"
            assert "\n" not in buf
            if indent + cursor + len(buf) <= MAX_LEN:
                return buf

        indent += INDENT_SIZE
        buf = "{\n" + " " * indent
        first = True
        for key, value in dct.items():
            if first:
                first = False
            else:
                buf += ",\n" + " " * indent
            if not isinstance(key, str):
                raise ValueError("Illegal key type '" + type(key).__name__ + "'")
            entry = '"' + key + '": '
            buf += entry + _encode(value, indent, len(entry))
        indent -= INDENT_SIZE
        buf += "\n" + " " * indent + "}"

        return buf

    def _encode(data, indent, cursor):
        if data is None:
            return "null"
        elif data is True:
            return "true"
        elif data is False:
            return "false"
        elif isinstance(data, (int, float)):
            return repr(data)
        elif isinstance(data, str):
            # Use the json module to escape the string with backslashes:
            return json.dumps(data)
        elif isinstance(data, (list, tuple)):
            return _encode_list(data, indent, cursor)
        elif isinstance(data, dict):
            return _encode_dict(data, indent, cursor)
        else:
            raise ValueError("Illegal value type '" + type(data).__name__ + "'")

    return _encode(o, 0, 0)
