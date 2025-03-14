---
layout: post
title: Dumping a traceback when an error message is printed
tags: [Software]

---

When a program I'm debugging prints something unexpected like an error message, I can usually search for a fragment of the message in the program's code to figure out why it was printed.

However sometimes I'm not able to locate the error message in the code at all! In that case one big hammer I have for isolating the offending code is to alter `print()`, `sys.stdout.write()`, and `sys.stderr.write()` to dump a traceback whenever a fragment of the error message is about to be printed:

```
altair (https://github.com/vega/altair)
+ <type_comment>:1: SyntaxWarning: invalid escape sequence '\('
+ 
+ *** Keyword 'SyntaxWarning' printed at:
+   File "/new_mypy/bin/mypy", line 10, in <module>
+     sys.exit(console_entry())
+   File "/new_mypy/mypy/__main__.py", line 15, in console_entry
+     main()
+   File "/new_mypy/mypy/main.py", line 156, in main
+     res, messages, blockers = run_build(sources, options, fscache, t0, stdout, stderr)
+   File "/new_mypy/mypy/main.py", line 240, in run_build
+     res = build.build(sources, options, None, flush_errors, fscache, stdout, stderr)
+   File "/new_mypy/mypy/build.py", line 191, in build
+     result = _build(
+   File "/new_mypy/mypy/build.py", line 267, in _build
+     graph = dispatch(sources, manager, stdout)
+   File "/new_mypy/mypy/build.py", line 2937, in dispatch
+     process_graph(graph, manager)
+   File "/new_mypy/mypy/build.py", line 3335, in process_graph
+     process_stale_scc(graph, scc, manager)
+   File "/new_mypy/mypy/build.py", line 3430, in process_stale_scc
+     mypy.semanal_main.semantic_analysis_for_scc(graph, scc, manager.errors)
+   File "/new_mypy/mypy/semanal_main.py", line 94, in semantic_analysis_for_scc
+     process_functions(graph, scc, patches)
+   File "/new_mypy/mypy/semanal_main.py", line 252, in process_functions
+     process_top_level_function(
+   File "/new_mypy/mypy/semanal_main.py", line 291, in process_top_level_function
+     deferred, incomplete, progress = semantic_analyze_target(
+   File "/new_mypy/mypy/semanal_main.py", line 351, in semantic_analyze_target
+     analyzer.refresh_partial(
+   File "/new_mypy/mypy/semanal.py", line 668, in refresh_partial
+     self.accept(node)
+   File "/new_mypy/mypy/semanal.py", line 7320, in accept
+     node.accept(self)
+   File "/new_mypy/mypy/nodes.py", line 818, in accept
+     return visitor.visit_func_def(self)
+   File "/new_mypy/mypy/semanal.py", line 926, in visit_func_def
+     self.analyze_func_def(defn)
+   File "/new_mypy/mypy/semanal.py", line 1007, in analyze_func_def
+     self.analyze_function_body(defn)
+   File "/new_mypy/mypy/semanal.py", line 1601, in analyze_function_body
+     defn.body.accept(self)
+   File "/new_mypy/mypy/nodes.py", line 1285, in accept
+     return visitor.visit_block(self)
+   File "/new_mypy/mypy/semanal.py", line 5272, in visit_block
+     self.accept(s)
+   File "/new_mypy/mypy/semanal.py", line 7320, in accept
+     node.accept(self)
+   File "/new_mypy/mypy/nodes.py", line 1641, in accept
+     return visitor.visit_with_stmt(self)
+   File "/new_mypy/mypy/semanal.py", line 5424, in visit_with_stmt
+     e.accept(self)
+   File "/new_mypy/mypy/nodes.py", line 1997, in accept
+     return visitor.visit_call_expr(self)
+   File "/new_mypy/mypy/semanal.py", line 5837, in visit_call_expr
+     self.try_parse_as_type_expression(a)
+   File "/new_mypy/mypy/semanal.py", line 7719, in try_parse_as_type_expression
+     t = self.expr_to_analyzed_type(maybe_type_expr)
+   File "/new_mypy/mypy/semanal.py", line 7355, in expr_to_analyzed_type
+     typ = self.expr_to_unanalyzed_type(expr)
+   File "/new_mypy/mypy/semanal.py", line 7418, in expr_to_unanalyzed_type
+     return expr_to_unanalyzed_type(
+   File "/new_mypy/mypy/exprtotype.py", line 202, in expr_to_unanalyzed_type
+     return parse_type_string(expr.value, "builtins.str", expr.line, expr.column)
+   File "/new_mypy/mypy/fastparse.py", line 327, in parse_type_string
+     _, node = parse_type_comment(f"({expr_string})", line=line, column=column, errors=None)
+   File "/new_mypy/mypy/fastparse.py", line 288, in parse_type_comment
+     typ = ast3_parse(type_comment, "<type_comment>", "eval")
+   File "/new_mypy/mypy/fastparse.py", line 142, in ast3_parse
+     return ast3.parse(
+   File "/usr/lib/python3.12/ast.py", line 52, in parse
+     return compile(source, filename, mode, flags,
+   File "/usr/lib/python3.12/warnings.py", line 113, in _showwarnmsg
+     _showwarnmsg_impl(msg)
+   File "/usr/lib/python3.12/warnings.py", line 30, in _showwarnmsg_impl
+     file.write(text)
+   File "/new_mypy/mypy/main.py", line 98, in write
+     traceback.print_stack(file=self.wrapped)
```

Notice that the dumped traceback points directly at the offending code.

Here's Python code which monkeypatches prints to dump a traceback whenever a particular substring is printed:

```
import sys
import traceback

def print_traceback_whenever_printed_line_contains(needle: str) -> None:
    """
    Replaces sys.stdout with a wrapper that inspects each write. If the output
    contains 'needle', a traceback is printed to the original sys.stdout.
    The monkeypatch remains in place after this function returns.
    """
    class PatchedStdStream:
        def __init__(self, wrapped):
            self.wrapped = wrapped

        def write(self, text: str) -> None:
            # Write text to the original stdout
            self.wrapped.write(text)

            # Check if 'needle' is in the text being written
            if needle in text:
                # Print a traceback to the original stdout
                self.wrapped.write(f'\n*** Keyword {needle!r} printed at:\n')
                traceback.print_stack(file=self.wrapped)

        def __getattr__(self, name: str):
            """
            Forward all other attributes (e.g., flush, fileno, isatty, etc.)
            to the original stdout.
            """
            return getattr(self.wrapped, name)

    sys.stdout = PatchedStdStream(sys.stdout)
    sys.stderr = PatchedStdStream(sys.stderr)

if __name__ == "__main__":
    # Activate the patch to watch for "ERROR" in any output
    print_traceback_whenever_printed_line_contains("ERROR")

    print("Everything is normal here...")
    print("Some random text with ERROR inside it!")
    print("Continuing after error message...")
```

Enjoy!
