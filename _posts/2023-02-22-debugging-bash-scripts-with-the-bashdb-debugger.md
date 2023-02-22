---
layout: post
title: Debugging bash scripts with the bashdb debugger
tags: [Software]
style: |
    .warning-box {
        background-color: #ffffe0; /* light yellow */
        border: 1px solid lightgray;
        padding: 5px;
    }
    .warning-box p {
        margin: 0;
    }

---

Sometimes when I have a problem with a bash script I want the ability to run each line of the script one by one to see what is wrong. There is a debugger called [bashdb] that can be used in this way. It behaves similarly to gdb (used for debugging C and C++ programs) and pdb (used for debugging Python programs).

[bashdb]: https://bashdb.sourceforge.net/

<!-- 
The following commands are tested in a Linux container created with:
    $ docker run -it --rm ubuntu:latest
-->

## How to install bashdb

First you need to determine what version of bash you are running, since you need to use a corresponding version of bashdb:

```
# bash --version
GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)
```

This version of bash is 5.1.16, so we need a bashdb version 5.1.x. Let's download it:

* For versions of bashdb <= 5.0.x, download from: <https://sourceforge.net/projects/bashdb/files/bashdb/>
* For versions of bashdb >= 5.1.x, you must download from the associated Git branch. For example bashdb 5.1.x is in git branch [bash-5.1](https://sourceforge.net/p/bashdb/code/ci/bash-5.1/tree/)

{% capture warning %}

NOTE: The following commands are written for an Ubuntu- or Debian-based Linux distribution. Also, you may need to prefix some commands with `sudo` to avoid permission errors.

{% endcapture %}
<div class="warning-box">{{ warning | markdownify }}</div>

```
# apt-get update
# apt-get install git -y
# git clone https://git.code.sf.net/p/bashdb/code bashdb-code
# cd bashdb-code/
# git checkout bash-5.1
```

For bashdb >= 5.1.x, you'll need to build the `configure` and `bashdb` files:

```
# apt-get update
# apt-get install autoconf -y  # to run autogen.sh
# apt-get install binutils -y  # to install "strings" tool, for autogen.sh
# apt-get install make -y  # to install "make" tool
# apt-get install texinfo -y  # to install "makeinfo" tool, for make
# ./autogen.sh
```

You should now have a `bashdb` file in the current directory:

```
# ls | grep bashdb
bashdb
bashdb-main.inc
bashdb-main.inc.in
bashdb-part2.sh
bashdb-trace
bashdb-trace.in
bashdb.in
```

(Optional) If you have root permissions, you can install bashdb:

```
# make install
```

## How to run bashdb

Let's create an example script to debug:

```
# cat << EOF > /tmp/hello.sh
echo 1
echo 2
echo 3
echo 4
EOF
```

If you did install bashdb in the step above, start the debugger on a Bash script at `/tmp/hello.sh` with:

```
# bash --debugger /tmp/hello.sh 
...
(/tmp/hello.sh:1):
1:	echo 1
bashdb<0> 
```

If you did not install bashdb, you can run the debugger by calling the bashdb script manually:

```
# bash ./bashdb /tmp/hello.sh 
...
(/tmp/hello.sh:1):
1:	echo 1
bashdb<0> 
```

## Common commands in bashdb

See all debugger commands using `help`:

```
bashdb<0> help
Available commands:
-------------------
  action     condition  edit     frame    load     run     source  unalias  
  alias      continue   enable   handle   next     search  step    undisplay
  backtrace  debug      eval     help     print    set     step+   untrace  
  break      delete     examine  history  pwd      shell   step-   up       
  clear      disable    export   info     quit     show    tbreak  watch    
  commands   display    file     kill     return   signal  trace   watche   
  complete   down       finish   list     reverse  skip    tty   

Readline command line editing (emacs/vi mode) is available.
Type "help" followed by command name for full documentation.
bashdb<1> 
```

See where you are in the script using `list`:

```
bashdb<1> list
  1: => echo 1
  2:    echo 2
  3:    echo 3
  4:    echo 4
  5:    
bashdb<2> 
```

You can **step over** the current line using `next` or `n`:

```
bashdb<3> next
1
(/tmp/hello.sh:2):
2:	echo 2
bashdb<4> list
  1:    echo 1
  2: => echo 2
  3:    echo 3
  4:    echo 4
  5:    
bashdb<5> 
```

You can **step into** the current line using `step` or `s`. This is useful to enter into a function call or a line that uses `source` to call another script:

```
bashdb<6> step
2
(/tmp/hello.sh:3):
3:	echo 3
bashdb<7> list
  1:    echo 1
  2:    echo 2
  3: => echo 3
  4:    echo 4
  5:    
bashdb<8> 
```

You can **step out** of the current function with `finish`.

Other common commands include:

* `eval STATEMENT` - Run a statement.
    * Example: `eval X=1`
* `print EXPR` - Print an expression, such as a variable.
    * Example: `print $X`
* `break` - Set a breakpoint.
    * Example: `break 3` (set breakpoint on line 3)
    * Example: `break /tmp/hello.sh:4` (set breakpoint on line 4 of file `/tmp/hello`)
* `continue`, `cont`, `c` - Step continuously until a breakpoint is hit or the script ends.
* `exit` - Stop the script and exit the debugger.
