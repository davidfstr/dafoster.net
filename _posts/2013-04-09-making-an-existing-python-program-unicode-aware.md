---
layout: post
title: Making an Existing Python Program Unicode Aware
tags: [Software]
x_date_written: 2012-11-07

---

Last week I decided to update one of my larger Python 2.7 projects to support Unicode fully
and to run under Python 3.

Here are the steps that I took and some gotchas I ran into along the way.

## General Strategy

Create and fully automate the unit test suite:

* This is important to detect any unexpected breakage from the Unicode-related changes you'll be making soon.
* Make sure your code coverage is good since tests can't protect you from mistakes introduced in uncovered code.

Identify all boundaries where data is being exchanged between the program and the outside environment. In my case:

* Direct I/O (i.e. `read` and `write`)
* Filesystem access (i.e. `open` and file paths)
* Process manipulation (via the `subprocess` module)
* Command-line arguments (via `sys.argv`)
* Time access (via the `time` module)

At boundaries:

* Reads should decode bytestrings to unicode using the proper encoding. You may need to do research to determine what the correct encoding is or how to determine the correct encoding at runtime.
    * Since my program did a lot of direct I/O on classic Mac OS data structures, the correct encoding was typically MacRoman.
    * `sys.getfilesystemencoding()` is sometimes appropriate. Be sure to test on Windows, where this value is typically not UTF-8.
* Writes should encode unicode (or ASCII bytestring literals) to bytestrings using the proper encoding.
* Ensure files and streams explicitly use either binary mode (i.e. `rb` or `wb`) or text mode (i.e. `rt` or `wt`).
    * UsuBytesIOally you want binary mode.
    * Text mode is required for certain cases, such as the output of the `json` module. Even then, it's a good idea to restrict text-based output to the ASCII character set since the native text encoding may not support the full Unicode set, particularly on Windows.

Finally:

* Run the `2to3` converter on your program so that it can be run by Python 3. 
* Run your new Python 3 source code in a Python 3 interpreter, perhaps inside a fresh Linux VM.
* Run your test suite under the Python 3 interpreter. It should find any Unicode mistakes that still need to be fixed.
* You will probably need to repeat this convert-test-fix cycle a couple of times.

## Special Cases

* Most uses of `StringIO` need to be migrated to `BytesIO`, when used as a byte buffer. If used as a string buffer, the `StringIO` uses need to be left at `StringIO`.
    * Here's the shim I used to support `BytesIO` and `StringIO` in both Python 2 and 3. I put it in a utility module and the rest of the program imports the shims instead of using the standard library.

<pre>
# BytesIO presents a stream interface to an in-memory bytestring.
# 
# This is equivalent to StringIO in Python 2 and to BytesIO in Python 3.
try:
    from io import BytesIO              # Python 3
except ImportError:
    from StringIO import StringIO as BytesIO

# StringIO presents a stream interface to an in-memory string
# (which is a bytestring in Python 2 and a unicode string in Python 3).
# 
# This is equivalent to StringIO in both Python 2 and 3.
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO             # Python 3
</pre>

* When writing to a binary stream, replace uses of `output.write(chr(byte_ordinal))` with `output.write(bchr(byte_ordinal))` and use the following shim for `bchr`:

<pre>
# bchr() converts the specified byte integer value to a single character
# bytestring.
# 
# This is equivalent to chr() in Python 2 but requires special handling in
# Python 3.
if bytes == str:
    def bchr(byte_ordinal):
        return chr(byte_ordinal)
else:
    def bchr(byte_ordinal):
        return bytes([byte_ordinal])    # Python 3
</pre>

* Beware of comparisons with `''`. Some of them probably need to be converted to comparisons with `b''`. For example, I had to adjust my `at_eof` utility function:

<pre>
def at_eof(input):
    """
    Returns whether the specified input stream is at EOF.
    """
    with save_stream_position(input):
        at_eof = input.read(1) == b''
    return at_eof
</pre>

* If your program uses human-readable ASCII bytestring literals, such as FourCC codes, make sure they are marked with the `b` prefix appropriately.

<pre>
if type_code == b'APPL':
</pre>

* Iteration over bytestrings works differently in Python 2 vs Python 3.
    * The code `for c in data:` will give back single-character bytestrings in Python 2 but byte ordinals in Python 3.
    * Here's my shim to let `for b in iterord(data):` always iterate over byte ordinals:

<pre>
# iterord() iterates over the integer values of the bytes in the specified
# bytestring.
if bytes == str:
    def iterord(bytes_value):           # Python 2
        for b in bytes_value:
            yield ord(b)
else:
    def iterord(bytes_value):           # Python 3
        return bytes_value
</pre>

* `time.strftime` returns a bytestring in Python 2 and a Unicode string in Python 3. Usually you want a Unicode string. I didn't create a shim for this since I only had one use of `strftime`.

<pre>
now_string = time.strftime('%b %d %H:%M', time.localtime(now))
if not isinstance(now_string, unicode):
    now_string = now_string.decode('ascii')
</pre>

* Regular expressions that are intended to apply to bytestrings instead of Unicode strings may need updating.
    * For example the pattern `re.compile(r'^Volume name is "(.*)"$')` which is designed to be applied to a MacRoman-encoded bytestring would need to be updated to read `re.compile(br'^Volume name is "(.*)"$')`

* Don't forget to update your documentation to specify where Unicode (or ASCII bytestring literals) are expected.