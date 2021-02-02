---
layout: post
title: Tests as Policy Automation
tags: [Software]

---

Automated tests are usually used for testing functional requirements of your product code. But they can *also* be used to enforce other policies and coding practices as well.

If writing a web application it's likely you already have a rule like "all automated tests must pass before any new version of the web application can be deployed to customers on the production environment". In that case any new policies you want to enforce regularly can be added to your standard automated test suite and they will necessarily have to be satisfied on every deployment!

Here are some example of special policies I've enforced from the automated test suite of [a large web application I work on] (which uses [Django], Python+[mypy], and JavaScript+TypeScript as core technologies):

[a large web application I work on]: /projects/techsmart-platform/
[Django]: https://www.djangoproject.com/
[mypy]: http://mypy-lang.org/index.html

{% capture test_outline %}
* Ensure the typechecker reports no errors
    * <code>test_type_checker_reports_no_errors_in_python</code>
    * <code>test_type_checker_reports_no_errors_in_typed_javascript</code>
* Ban unsafe coding patterns by inspecting source code
    * <code>test_no_new_fragile_test_suites</code>[^fragile-test-suites]
    * <code>test_ensure_all_directories_containing_py_files_have_init_file</code>[^no-init-file]
* Ensure hard-coded debug modes are turned off
    * <code>test_the_debug_toolbar_is_disabled</code>
    * <code>test_that_compress_is_enabled</code>
* Ensure test-only environmental settings are correctly configured
    * <code>test_that_tests_do_not_send_real_emails</code>
* Ensure invariants that should apply to all types of a large/unbounded number of domain objects are satisfied:
    * <code>test_all_django_add_and_edit_admin_pages_render</code>
    * <code>test_every_block_type_satisfies_all_block_standards</code>
        * <code>test_c_blocks_for_python_blocks_must_use_consistent_indent_width</code>
        * <code>test_every_field_id_must_use_underscore_case</code>
        * <code>test_every_block_type_whose_codegen_always_references_x_library_must_import_x_library</code>
        * ... (9 more)
* Prevent certain configuration settings from changing without triggering a discussion with Product Management, the Business, or your Dev Lead
    * <code>test_max_redirect_count_is_5</code>
{% endcapture %}
{{ test_outline | break_after_underscores }}

Hopefully these examples give you some ideas of some special policies you might enforce in your own automated test suite. Happy coding!

[^fragile-test-suites]: In this context a "fragile test suite" corresponds to a subclass of Django's `StaticLiveServerTestCase` or `TestCase` whose `setUpClass` method fails to use a `try-finally` to invoke `super().tearDownClass()` explicitly if something goes wrong partway through the test suite setup. This fragile-detection metatest walks through all test suite classes and uses Python's `inspect.getsourcelines` to read the source code of all test classes to look for the absense of the proper kind of try-finally.

[^no-init-file]: It is important for any directory containing Python source files (`*.py`) to contain an `__init__.py` file so that the directory is marked properly as a Python package and is recognized correctly by Python typecheckers like mypy.

### *Related Articles*

* <a href="https://sirupsen.com/shitlists/" class="external">Shitlist Driven Development</a> - Gives techniques for how to effectively apply automated policy changes of the type discussed in this article at *large* scale.
<!-- * [Performance Testing](/articles/2018/06/02/performance-testing/) -->
* [Database clamps: Deterministic performance tests for database-dependent code](/articles/2021/02/09/database-clamps-deterministic-performance-tests-for-database-dependent-code/) - *Next week's article* 🙂