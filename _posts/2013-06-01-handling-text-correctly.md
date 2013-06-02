---
layout: post
title: Handling Text Correctly
tags: [Software]
x_date_written: 2011-05-18

style: |
  /* Horizontal scrolling code blocks */
  pre      { overflow-x: auto; word-wrap: normal; }
  pre code { white-space: pre; }
  
  /* Prevent word breaks for "UTF-8" and similar phrases */
  .nobr { white-space: nowrap; }

---

<div style="padding: .8em 1em .8em; margin-bottom: 1em; border: 1px solid #94da3a;">
    <p style="font-weight: bold; color: #487858;">
        Series
    </p>
    <p style="margin-bottom: 0em;">
        This article is part of the <a href="/articles/2013/05/11/book-outline/">Programming for Perfectionists</a> series.
    </p>
</div>

<div class="toc">
  <ul>
    <li><a href="#characters-sets-and-encodings">Characters, Sets, and Encodings</a></li>
    <ul>
      <li><a href="#important-character-sets">Important Character Sets</a></li>
      <li><a href="#unicode">Unicode</a></li>
      <ul>
        <li><a href="#unicode-character-encodings">Unicode Character Encodings</a></li>
      </ul>
    </ul>
    <li><a href="#common-mistakes-and-practical-tips">Common Mistakes &amp; Practical Tips</a></li>
    <ul>
      <li><a href="#you-cannot-interpret-a-byte-array-as-a-string-without-knowing-its-encoding">You cannot interpret a byte array as a string without knowing its encoding.</a></li>
      <ul>
        <li><a href="#reading-text-files">Reading Text Files</a></li>
        <li><a href="#converting-between-bytes-and-strings">Converting Between Bytes and Strings</a></li>
      </ul>
      <li><a href="#a-char-in-your-favorite-language-is-probably-not-a-character">A "char" (in your favorite language) is probably not a character.</a></li>
      <ul>
        <li><a href="#8-bit-chars">8-bit chars</a></li>
        <li><a href="#16-bit-chars">16-bit chars</a></li>
        <li><a href="#32-bit-chars">32-bit chars and variable-bit chars</a></li>
      </ul>
    </ul>
    <li><a href="#end-of-line-sequences">End of Line Sequences</a></li>
    <li><a href="#summary">Summary</a></li>
  </ul>
</div>

{% capture Alert %}⚠{% endcapture %}

<a id="characters-sets-and-encodings"></a>
## Characters, Sets, and Encodings

Text is made up of multiple **characters** (or **codepoints**[^Codepoint]), each of which represents a different letter, symbol or punctuation mark. The word "Hello", for example is made of the characters "H", "e", "l", "l", and "o". This collection of characters is called a **string**. Each character is assigned a number using a **character set** (sometimes called a *code page* or a *charset*).

For example the **ASCII** character set assigns numbers in the range (0-127) for characters in most Western European languages.

<div style="font-size: 20px; margin-left: 3em; font-family: monospace; margin-bottom: 12px; line-height: 1.1em;">
H &rarr; 72<br/>
e &rarr; 101<br/> 
l &rarr; 76<br/>
l &rarr; 76<br/>
o &rarr; 111
</div>

ASCII is one of the oldest character sets. Most other sets use the same mappings as ASCII, while defining additional mappings of their own for numbers above 127.

After mapping a character to a number, that number is converted to an actual byte sequence for storage. The entire process of converting a character to a byte sequence is defined by a **character encoding**.

Since many character sets provide mappings to numbers in the range 0-255 (which fit in 8-bit bytes), you can output the character number as a single byte. For example, to output "Hello" in ASCII, you would emit the byte sequence:

H  | e   | l  | l  | o
---|-----|----|----|----
72 | 101 | 76 | 76 | 111

Many English-speakers, being only familiar with the Western European character sets which are always encoded with individual 8-bits bytes, often use the terms *character set* and *character encoding* interchangably.

However the East Asian languages such as Chinese, Japanese, and Korean (CJK) have many more than 256 characters, making it impossible to fit them in only 8-bit bytes. Therefore each character must be encoded using multiple bytes, possibly a variable number of bytes. Thus either a fixed-width encoding (often 16-bits per character) or a variable width encoding (with differing numbers of bytes per character) may be used.

[^Codepoint]: To be precise, the definition of *character* used here is exactly the same as a *Unicode codepoint*, for those readers who are already familiar with Unicode.

<a id="important-character-sets"></a>
### Important Character Sets

The following are the most prevalent non-Unicode character sets you are likely to encounter. All of these character sets are encoded with a single byte per character.

Character Set                   | Character Encoding 
--------------------------------|--------------------------
ASCII                           | single byte (7-bit)
Windows-1252 (Windows Latin 1)  | single byte
ISO 8859-1 (ISO Latin 1)        | single byte
Mac OS Roman                    | single byte

Informally (and in practice), these may also be described as character encodings. So a text file "in ASCII encoding" refers to a file in the ASCII character set with its standard single-byte encoding.

* **ASCII**
    - 7-bit character set for representing characters common to most Western European languages.
    - <p>{{ Alert }} Many programs and APIs that claim to input or output "ASCII" (or "ANSI"[^ANSI]) are actually unaware of character sets and will accept strings in whatever the operating system's default character set happens to be (often Windows-1252).</p>
* **Windows-1252** (AKA **Windows Latin 1**)
    - <p>This is the default character set on English Windows systems.</p>
* **ISO 8859-1** (AKA **ISO Latin 1**)
    - The default character set for web pages and other HTTP traffic.
    - <p>{{ Alert }} In practice this is *very* frequently confused with <b>Windows-1252</b>, which differs in only a handful of characters. In fact this confusion is to such a degree that the draft HTML 5 specification requires that documents advertised as ISO-8859-1 actually be parsed as Windows-1252.[^HTML5]</p>
* **Mac OS Roman**
    - This is the default character set on most Macintosh systems prior to Mac OS X.

Not every character set can represent every character in the world. For example Windows-1252 cannot represent any Chinese or Japanese characters, although GBK and Shift JIS respectively can. This means that you cannot in general mix text from two sources that uses a different character sets without converting to a new character set (that can represent all characters in both sets). Typically the Unicode character set (discussed below) is used for this purpose.

[^ANSI]: Windows documentation often refers to the default character set (or sometimes the ASCII character set) as the "ANSI encoding". This is misleading since this is not a single concrete encoding and has nothing to do with the ANSI standards body. For example, the Save dialog in Windows Notepad (in Windows 7) and <a href="http://msdn.microsoft.com/en-us/library/cc231241(v=prot.10).aspx">Unicode Versus ANSI String Representations</a> use "ANSI" to refer to the default encoding, whereas <a href="http://msdn.microsoft.com/en-us/library/aa368046(v=vs.85).aspx">Copy a Unicode File to an ANSI File</a> uses "ANSI" to refer to the ASCII encoding.

Character Set                           | Character Encoding 
----------------------------------------|--------------------------
Windows-932 ("Shift JIS")<!--[^WStd]--> | variable width, 1-2 bytes
Windows-936 ("GBK")                     | variable width, 1-2 bytes

[^HTML5]: [HTML 5 Draft Recommendation — 12 April 2010, 8.1 Character encodings](http://dev.w3.org/html5/spec/Overview.html#character-encodings-0), retrieved 2010-04-12.

<!--
[^WStd]: It should be noted that that the official Shift JIS and GBK specifications differ from their implementations in Windows. However it is the Windows implementations that have become the de-facto standards. Therefore if you see an unqualified reference to "Shift JIS", it most likely refers to Windows-932 instead of the official standard.
-->


<a id="unicode"></a>
### Unicode

**Unicode** is a character set just like ASCII or Windows-1252: it maps characters to numbers.[^UnicodeDef] However it is sufficiently important to justify special mention.

The Unicode character set is designed to support all characters in all character sets that came before it, plus many more. If you can think of a character, it's almost certainly in Unicode. (And if it isn't, it's likely not in any character set.) In this sense, Unicode can be viewed as the universal character set.

> Any program written today that wishes to represent characters correctly should be using the Unicode character set and one of its associated encodings.

Originally, Unicode mapped characters to numbers in the range 0x0000-0xFFFF, requiring only 16 bits to represent each character. At that time it was possible to encode each Unicode character using a 2-byte fixed width encoding, known as **UCS-2**. Many early Unicode-aware systems, such as Java, were designed around this original specification.

In 1996, Unicode was extended to map characters to numbers in the larger range of 0x00000-0x10FFFF, requiring up to 20 bits per character. Thus UCS-2, being limited to 16-bits, was no longer capable of representing all Unicode characters. In its place arose the **UTF-16** encoding which, like UCS-2, uses a single 16-bit value to represent characters in range 0x0000-0xFFFF (the **basic multilingual plane**) and two 16-bit values to represent characters in range 0x10000-0x10FFFF (the **supplemental plane** or **astral plane**). And so many UCS-2 systems were retroactively upgraded to use UTF-16 in place of UCS-2.

Today, UTF-16 is the most common in-memory representation for Unicode strings. However, many programs incorrectly treat individual 16-bit values from UTF-16 directly as characters, due to ignorance of UTF-16's variable-width nature. In many cases this causes no problems, since most programs operate on strings and substrings opaquely, as opposed to working with individual characters. However problems will arise if unaware programs attempt to manipulate characters directly, such as by counting the number of characters in a string or by filtering individual characters.

[^UnicodeDef]: The full Unicode standard also covers a wide variety of rules related to handling characters, such as sorting, rendering, and other operations. For our purposes though, we are only concerned with the Unicode character set.

<a id="unicode-character-encodings"></a>
#### Unicode Character Encodings

Unlike the other character sets discussed previously, the Unicode character set has *multiple* different encodings.

Character Set   | Character Encoding    | Character Encoding Scheme
----------------|-----------------------|------------------------------
Unicode         | UTF-8                 | variable width, 1-4 bytes
                | UCS-2                 | fixed width, 2 bytes
                | UTF-16                | variable width, 2 or 4 bytes
                | UTF-32 / UCS-4        | fixed width, 4 bytes

* **UTF-8**
    - This is the default on-disk encoding for most modern Unicode-aware programs.
        - Many text editors save in this format by default.
        - Python 2.5+ source files are assumed to be UTF-8 by default.
    - It can represent any character in the Unicode character set, and thus any character in the world.
    - It is compact, representing all ASCII characters as single bytes and most other characters as two bytes.
    - <p>{{ Alert }} Programs may optionally prepend a **byte-order-mark (BOM)** at the beginning of a file to mark it as UTF-8. Most Windows programs do this, for example. Programs that input <span class="nobr">UTF-8</span> files should be prepared to handle BOMs.</p>
* **UCS-2**
    - This is the native encoding used by early Unicode-aware systems, such as Java 1.4 and below.
    - It can only represent Unicode characters in the basic plane (0x0000-0xFFFF), but no higher.  
      In particular characters in the supplementary planes (0x10000-0x10FFFF), sometimes known as **astral characters**, cannot be represented.
    - <p>Many APIs that originally only supported UCS-2 were retroactively upgraded to use <span class="nobr">UTF-16</span>.</p>
* **UTF-16**
    - This is the default in-memory encoding for most modern Unicode-aware systems, including Windows, Mac OS X, the Java 1.5+ runtime[^JavaUTF16], the .NET runtime (including C#), and Python 2.x[^PEP261].
    - It can represent any character in the Unicode character set.
    - Characters in the basic plane (0x0000-0xFFFF) are encoded as a single 16-bit value.  
      Astral characters (0x10000-0x10FFFF) are encoded as two 16-bit **surrogate** values.
    - {{ Alert }} It is common for code to incorrectly manipulate UTF-16 data as if it were fixed-width <span class="nobr">UCS-2<span> instead.
    - {{ Alert }} Programs may optionally prepend a *byte-order-mark (BOM)* at the beginning of a file to mark it as UTF-16 or to specify a byte-ordering other than big-endian. Programs that input <span class="nobr">UTF-16<span> files should be prepared to handle BOMs.
    - <p>{{ Alert }} Some outdated documentation and APIs may refer to the UTF-16 encoding as the "Unicode encoding". Notably C#'s <a href="http://msdn.microsoft.com/en-us/library/system.text.unicodeencoding.aspx">UnicodeEncoding</a>, Mac OS X's <a href="http://developer.apple.com/library/mac/documentation/Cocoa/Reference/Foundation/Classes/NSString_Class/Reference/NSString.html#//apple_ref/doc/c_ref/NSUnicodeStringEncoding">NSUnicodeStringEncoding</a> or Python 2.2-3.2's `unicode` type on "narrow" builds, which are the default.</p>
* **UTF-32 / UCS-4**
    - This is a fixed width encoding capable of representing any Unicode character directly as a 32-bit value.
    - Because it is space inefficient, this encoding is rarely seen in practice.
        - Python 2.2-3.2 offers "wide" builds use UTF-32.
    - {{ Alert }} Programs may optionally prepend a *byte-order-mark (BOM)* at the beginning of a file to mark it as UTF-32 or to specify a byte-ordering other than big-endian. Programs that input <span class="nobr">UTF-32</span> files should be prepared to handle BOMs.

[^JavaUTF16]: Compare the documentation for java.lang.String between [Java 1.4](http://docs.oracle.com/javase/1.4.2/docs/api/java/lang/String.html) and [Java 1.5](http://docs.oracle.com/javase/1.5.0/docs/api/java/lang/String.html). The 1.5 documentation clearly states UTF-16 as the internal string encoding.

[^PEP261]: <a href="http://www.python.org/dev/peps/pep-0261/">PEP 261</a> describes Python 2.x's Unicode handling with respect to characters in the supplementary planes. "Narrow" Python builds (the default) use UTF-16 internally; "wide" Python builds use UTF-32 internally. (The distinction between narrow and wide builds disappeared in Python 3.3.)


<a id="common-mistakes-and-practical-tips"></a>
## Common Mistakes & Practical Tips

<a id="you-cannot-interpret-a-byte-array-as-a-string-without-knowing-its-encoding"></a>
### You cannot interpret a byte array as a string without knowing its encoding.

<a id="reading-text-files"></a>
#### Reading Text Files

You cannot read a text file correctly without knowing its encoding.

If you do not specify an encoding explicitly when opening a text file, your language's standard library or operating system will usually pick a default encoding, which depends on the spoken language it is running in, among other factors.

Unfortunately most filesystems do not store the encoding of a text file.[^HFS-encoding] So there are a few options for determining an encoding:

* **Define a particular encoding as the expected input.**
    - <p>For example, a receipt-processing program may explicitly document UTF-8 as the encoding for its input files.</p>
* **Look at the contents of the input file to auto-detect the encoding:**
    * You could detect UTF byte-order-marks at the beginning of a file to automatically assume one of the UTF encodings.
    * You could define a special syntax at the beginning of the input files to indicate the encoding.
        - XML uses a prelude at the top of a file to indicate what encoding it uses. For example `<?xml version="1.0" encoding="windows-1252"?>` specifies that the document is in Window-1252 encoding. (Of course to even read this initial text, you have to make the working assumption that the top of the file is some encoding that is a superset of ASCII.)
        - Python source files use a line such as `# -*- coding: utf-8 -*-` to indicate the encoding is other than the default. (Python 2.0-2.4 uses Windows Latin 1 as the default encoding; Python 2.5-2.7 uses ASCII, Python 3.x uses UTF-8.)
    * <p>Failing these options, you could fall back to a defined encoding (such as ASCII for Python source files) or to the operating system's default encoding (which can vary).</p>
* **Always use the operating system's default encoding.**
    - This is often the behavior if you use your favorite programming language's default mechanism for reading a file, such as Java's `FileReader` class. (Interestingly, C#'s `StreamReader` and `StreamWriter` classes always use UTF-8 instead of the operating system default.)

[^HFS-encoding]: The HFS filesystem used in Mac OS 9 and Mac OS X is one of the few filesystems that stores the encoding of text files as file metadata. However I think almost no modern OS X program is aware of this.

<a id="converting-between-bytes-and-strings"></a>
#### Converting Between Bytes and Strings

You cannot correctly convert a byte array to a string without specifying the encoding to use.

Unfortunately many languages allow you to omit the encoding, and then will try to guess the encoding (usually incorrectly) if you fail to specify it.

Consider the following Java program:

```
byte[] goodbyeBytes = {'T', 's', 'c', 'h', \uC3BC, \uC39F, '!'};
String goodbyeString = new String(goodbyeBytes);              // WRONG: OS-dependent
```

This program will decode different strings on different operating systems! On Mac OS X and Linux where the platform's default charset is UTF-8, the correct result ("Tschüß!") will be obtained since the original bytes were encoded in UTF-8. However on Windows the bogus result "TschÃ¼ÃŸ!" will be decoded because the default charset is Windows-1252.

Here's the fixed program, which specifies the UTF-8 charset explicitly:

```
byte[] goodbyeBytes = {'T', 's', 'c', 'h', \uC3BC, \uC39F, '!'};
String goodbyeString = new String(goodbyeBytes, "UTF-8");     // CORRECT
```

As another example, consider the Java `InputStreamReader` and `FileReader` classes, both of which convert from byte streams to character streams.

```
byte[] goodbyeBytes = {'T', 's', 'c', 'h', \uC3BC, \uC39F, '!'};
InputStream goodbyeStream = new ByteArrayInputStream(goodbyeBytes);
Reader goodbyeReader = new InputStreamReader(goodbyeStream);  // WRONG: OS-dependent
```

Or the even more innocent-looking:

```
Reader goodbyeReader = new FileReader("goodbye.txt");         // WRONG: OS-dependent
```

Both of these examples are wrong for the same reason: they don't specify the encoding. And both can be fixed by adding `"UTF-8"` as the second argument to the appropriate constructor.

Of course the same problems happen when encoding a string to a byte stream:

```
String goodbyeString = "Tschüß!";
byte[] goodbyeBytes = goodbyeString.getBytes();               // WRONG: OS-dependent
```

And when encoding a character stream to a byte stream:

```
ByteArrayOutputStream goodbyeStream = new ByteArrayOutputStream();
Writer goodbyeWriter = new OutputStreamWriter(goodbyeStream); // WRONG: OS-dependent
goodbyeWriter.write("Tschüß!");
byte[] goodbyeBytes = goodbyeStream.toByteArray();
```

And when writing to text files:

```
Writer goodbyeWriter = new FileWriter("goodbye.txt");         // WRONG: OS-dependent
goodbyeWriter.write("Tschüß!");
```

<a id="a-char-in-your-favorite-language-is-probably-not-a-character"></a>
### A "char" (in your favorite language) is probably not a character.

Many programming languages have a "char" datatype that is intended for representing a character. Usually this "char" datatype could do this effectively at the time the language was written but not in the present day, as the notion of a character has been extended over time.

<a id="8-bit-chars"></a>
#### 8-bit chars (C/C++)

In C/C++, a "char" holds one byte. When C was first invented, 8-bit fixed-width character encodings were the norm. Therefore a single "char" was able to represent a single character precisely. However with the advent of CJK languages and multi-byte encodings, this no longer worked. Therefore a C string by itself today can only be safely interpreted as a raw byte stream. As mentioned above, you can only process it properly if you know what encoding it is in.

Without any further information, C string is often assumed to be in the operating system's default encoding, although you cannot be sure. The correct encoding to use depends on where the string was input from.

A program can work with strings in a few ways:

* <p>**Choose a particular in-memory encoding that all functions should use.**</p>
    + <p>All foreign strings will be converted to this encoding at the time of input (regardless of source). And upon output, strings will be converted to the appropriate proper output encoding.</p>
    + <p>UTF-8 and UTF-16 are both good candidates for such an in-memory encoding since they can both represent the full repertoire of Unicode characters. Therefore you won't lose any data by converting to/from them.</p>
        - <p>UTF-8 is compact and a superset of ASCII, so you can pass UTF-8 strings to brain-dead functions that are encoding unaware and get correct behavior as long as only ASCII characters are being used.</p>
        - <p>UTF-16 is convenient because functions that are unaware of astral characters will still get correct behavior as long as basic-plane Unicode characters are used, which are the most common.</p>
* **Pass around the text encoding around with the underlying byte array, possibly with a custom string datatype.**
    - No encoding conversion overhead with reading the input stream.
    - Cannot mix text with different encodings.
    - <p>Ruby takes this approach with its built-in `String` type.</p>
* **Blithely ignore encoding issues altogether and get unexpected results when working with international characters.**
    - Many programs written in languages where the default string type in not Unicode take this option out of ignorance. In particular this includes many programs in C, PHP, and <span class="nobr">Python 2.x</span>.

Gotchas:

* Beware of methods that take exactly one `char` or return exactly one `char`.  
    * They almost certainly aren't aware of non-ASCII or Unicode characters.
* Beware of any libraries that don't document what text encoding it assumes.
    * They almost certainly aren't aware of non-ASCII or Unicode characters.

<a id="16-bit-chars"></a>
#### 16-bit chars (Java, C#, Objective-C, Python 2.2-3.2, C/C++'s `wchar`)

Java and C#'s `char` are 16-bits wide. So are C/C++'s `wchar` and Mac OS X's `unichar`. And so are the elements of a Python 2.x string when it is compiled in the default "narrow" mode.

16-bits is sufficient to hold a Unicode character in the basic plane (0x0000-0xFFFF) but not an astral character in a supplemental plane (0x10000-0x10FFFF). In the case of these languages, a `char` represents a single UTF-16 code unit (i.e. either a character in the basic plane or a surrogate) as opposed to an actual character.

Therefore text-aware programs in these languages need to be particularly careful to deal with astral characters correctly, since those characters cannot fit into a single `char` variable.

Here is a typical Java program that is unaware of astral characters:

```
String str = "Hello";
for (int i=0, n=str.length(); i<n; i++) {
    // WRONG: Does not handle characters outside the basic plane (0x0000-0xFFFF)
    char c = str.charAt(i);
        
    // ... Do something with the character, like filtering out invalid characters.
}
```

And here is a much-longer but correct version that correctly identifies surrogates and decodes them to astral characters correctly:

```
String str = "Hello";
for (int i=0, n=str.length(); i<n; i++) {
    char c1 = str.charAt(i);
    
    // CORRECT. Handles all Unicode characters.
    int codepoint;
    if (Character.isHighSurrogate(c1)) {
        if (i+1 < n) {
            char c2 = str.charAt(i+1);
            if (Character.isLowSurrogate(c2)) {
                // Surrogate pair
                codepoint = Character.toCodePoint(c1, c2);
                
                i++;
            } else {
                // High-surrogate alone
                codepoint = (int) c1;
            }
        } else {
            // High-surrogate alone at end of string
            codepoint = (int) c1;
        }
    } else {
        // Not a surrogate pair
        codepoint = (int) c1;
    }
    
    // ... Do something with the character, like filtering out invalid characters.
}
```

Gotchas:

* Beware of methods that take exactly one `char` or return exactly one `char`.  
    * They almost certainly aren't aware of astral characters.
* You can't iterate over the characters in a "string" by iterating over the `char`s.
    * Instead you have to use a loop like the above to iterate over the true characters.  
      This example stores the true character in the `codepoint` variable.
* You can't get the i<sup>th</sup> character of a "string" by getting the i<sup>th</sup> `char`.
    * No general workaround.


<a id="32-bit-chars"></a>
#### 32-bit chars and variable-bit chars (Python 3.3+, Haskell)

If you're fortunate enough to work in an environment with 32-bit or variable-bit chars then your `char` is in fact a character. Horray!

The only popular environment I know of with real characters is Python 3.3+, or Python 2.2-3.2 when configured to be in "wide" mode (which is not the default).


<a id="end-of-line-sequences"></a>
## End of Line Sequences

Improper handling of end-of-line (EOL) sequences is not uncommon.

There are three common ways to end a line:

* Linux: `\n` (line feed alone)
* Windows: `\r\n` (carriage return + line feed)
* Mac OS 9: `\r` (carriage return alone)

It is possible for multiple styles to occur in the same file or string.

It should also be noted that the last line in a file or string might or might not be followed by an EOL sequence. Therefore you can't assume that every line ends with an EOL sequence.

As the following examples demonstrate, you need to read your language's documentation carefully if you want to process lines in a consistent fashion.

#### Java Line Reader Example

Consider the following Java program:

```
// Prints the specified file to standard output.
public static void main(String[] args) {
    String filePath = args[0];
    BufferedReader lineReader =
        new BufferedReader(new FileReader(filePath, "UTF-8"));
    try {
        String nextLine;
        while ((nextLine = lineReader.readLine()) != null) {
            System.out.println(nextLine);
        }
    } finally {
        lineReader.close();
    }
}
```

The `BufferedReader` class can deal with all end-of-line sequences. Therefore this program is resilient against mixed input.

However `println` (in the `PrintWriter` class) emits the OS-specific end-of-line sequence, which means that this program will have different output on different operating systems. Not necessarily what you'd expect.

#### Python 2.x Line Reader Example

Consider the following Python 2.x program:

```
import codecs

file_path = sys.argv[1]
with codecs.open(file_path, 'rb', 'utf-8') as stream:
    for line_with_terminator in stream:
        line = line_with_terminator.rstrip(u'\r\n')    # remove any trailing '\r' and '\n's
        print line
```

Notice that in the Python version it is necessary to explicitly remove the `\r` and `\n` characters, since Python's line iteration behavior is to return the entire line plus the end-of-line sequence (if available).

Python's `print` statement always uses `\n` as the end-of-line sequence, regardless of what OS it is running on. It's nice that this is a consistent behavior, but it might not be what you expect if you are developing on Windows.

Here is perhaps a more typical program that fails to handle the last line correctly if it doesn't end with an EOL sequence:

```
import codecs

file_path = sys.argv[1]
with open(file_path, 'rU') as stream:     # the U mode converts all line endings to '\n'
    for line_with_terminator in stream:
        # WRONG: If last line lack an EOL this will chop off its trailing character improperly
        line = line_with_terminator[:-1]  # remove trailing '\n'
        # WRONG: Treating a bytestring as if it were a Unicode string
        print line
```

Errors like this explain why lots of Unix programs warn about or get confused by files that don't end with a final EOL.

And here is another typical variation that does not handle end-of-line sequences properly:

```
import codecs

file_path = sys.argv[1]
with open(file_path, 'rb') as stream:
    for line_with_terminator in stream:
        # WRONG: Assumes EOL is one byte long, which is incorrect on Windows
        line = line_with_terminator[:-1]  # remove trailing '\n'
        # WRONG: Treating a bytestring as if it were a Unicode string
        print line
```

This kind of program will get extra `\r` characters on the end of each line when run on Windows. It also fails to handle final lines that lack an EOL.

<a id="summary"></a>
## Summary

Working with text is tricky. Your programming language probably has default handling that isn't quite what you want (or expect) so always read the documentation carefully. And if your program is intended to be usable in multiple languages, you actually should write tests that check for proper handling of Unicode characters.
