---
layout: post
title: You might not need centralized continuous integration
tags: [Software]
x_audience: |
    Any developer who seeks to build high-quality software,
        especially "perfectionists with deadlines" :)
x_performance: |
    TODO

---

The general availability of easy-to-use centralized **continuous integration**[^continuous integration] (CI) solutions in recent years - from GitHub Actions[^github-actions] and Travis as hosted solutions, and from Jenkins[^jenkins] and Hudson as on-premises solutions - has been wonderful for allowing software to be tested continuously throughout development, catching errors early *before* changes are merged to shared development and mainline branches.

[^continuous integration]: <https://docs.microsoft.com/en-us/azure/devops/learn/what-is-continuous-integration>

[^github-actions]: [GitHub Actions](https://docs.github.com/en/actions) is my favorite hosted continution integration solution at the moment, replacing the formerly-excellent Travis, which has become unfriendly to open-source development in recent years.

[^jenkins]: [Jenkins](https://www.jenkins.io/doc/) is the venerated and popular self-hosted continuous integration server that's been around for the last decade or so.

Today I'd like to explore the now perhaps-controversial idea of "When might it *not* be worth the effort to setup a centralized continuous integration service?" In particular I've somehow managed to *not* setup a CI server for the primary web app I've been developing and running in production even after several years.<!--[^ts-platform]-->

<!-- [^ts-platform]: In case you're curious, the web app I mentioned that I've been developing for several years that currently lacks *centralized* continuous integration is the [TechSmart Platform](/projects/techsmart-platform/) for online computer science learning and coding. -->

## The wonders of continuous integration

First, I want to dispel any notion that I'm against the idea of continuous integration in general. Nothing could be further from the truth: Continuous integration - automatically running a project's test suite against smaller branches in version control that are pending merge to a larger branch - is extremely valuable to detect new bugs as early as possible, before they reach customers and before they even reach other members of your development team. Detecting bugs early helps you ship high-quality software faster.

## The trouble with *centralized* continuous integration

That being said, *centralized* continuous integration, where there's a single dedicated service or server that is responsible for running CI jobs, can be complex to setup. If you're setting up CI for a project that has only a command-line interface, is an API, or is otherwise *functional* in design, then you should just stop here and go setup centralized CI for your project. For those cases it's generally not that hard to setup these days. On the other hand if you're trying to setup CI for a graphical program or something like a website that requires UI testing, then getting CI setup can be much more tricky.

Now it is absolutely *possible* to get CI setup for a project that requires graphical testing, it's just a lot of work: You'll probably need to automate the creation of a VM with the target operating system (through a Docker container for Linux, or a true VM for Mac or Windows), build & install the latest project version from source, install related web browsers and other UI tools, and setup some kind of remote graphical access (through VNC for Linux or Mac, or Remote Desktop for Windows) to debug any test failures that only occur during the CI process.

## Alternative: *Distributed* [^distributed-ci] continuous integration

[^distributed-ci]: I call this approach *distributed* continuous integration because it is distributed across your team's development machines, rather than relying on being run on a central CI server or "build box".

Here's another idea: You already have a test suite that runs on your development machines right? What if you were to just lean on that existing process for your CI needs?

In particular the thought is that you would make it a policy to regularly run the full test suite at certain intervals, perhaps before merging a feature branch in version control to the development branch. Or perhaps before merging the development branch to the mainline branch released to end-users and production.

How might you enforce such a policy? Well, you likely already have a custom tool that helps you merge & release the development branch to end-users that already runs on your local development machine. What if you just add a step to that tool that runs the test suite, and have the tool only continue if the tests pass? Easy right?

Of course any sufficiently large test suite - especially one interacting with a GUI or a live network - will have at least a few flaky tests that fail occasionally and cannot be fixed immediately. So there should still be a way for a developer to quickly rerun any (flaky) tests that fail so that they hopefully pass, and the developer can manually certify that all tests did eventually pass. To manually certify that all tests did pass on a particular commit, a developer could be required to manually "sign off" on the testing by typing out part of the commit's hash, perhaps just the first few characters of it.

## Putting it all together <small>An example distributed continuous integration system</small>

Given the design above, what might an implementation of a distributed continuous integration system look like in practice? Here's what it looks like for my primary web app, a Django-based rich web application:

Let's say I'm on the tip of our development branch (`develop`) and want to merge into the mainline branch (`main`) and deploy to production. My Git history might look like:

```
* a8affa5f7 <David Foster> - (main) Hotfix
| * bd8821196 <David Foster> - (HEAD -> develop) Feature D
| * 26adfda55 <David Foster> - Feature C
|/  
* b005bfee9 <David Foster> - Deploy to production.
|\  
| * 77e0fc2a1 <David Foster> - Feature B
| * d6f29d264 <David Foster> - Feature A
|/ 
* 588e5e61b <David Foster> - Deploy to production.
```

To merge I'd run our special-purpose `mergedeploy` command:

```
$ python3 manage.py mergedeploy
Merging: main <- develop
Pulling trunk and feature branches...
Creating merge commit...
Running tests...
  Log: /var/folders/vm/nd6nhd948xj4ds001s76srj80000gn/T/mergedeploy-fabs0_mt.log
CommandError: Tests failed.
Fix, commit the fix, and run: pm mergedeploy --continue
Or abort with: pm mergedeploy --abort
```

Inspecting the log I see:

```
Creating test database for alias 'default'...
System check identified no issues (1 silenced).
......ssssssssssssssssssssssssssssssssssssssssssssF..........
----------------------------------------------------------------------
Ran 61 tests in 16.154s

FAILED (failures=1)
Destroying test database for alias 'default'...

Rerun failed tests with:
$ python3 manage.py test \
    ide.tests.PerformanceTests.test_mouse_move_near_top_of_large_program_is_fast_enough
```

Looks like there's a single failing non-deterministic performance test that's likely to be flaky. Let's rerun it:

```
$ python3 manage.py test \
    ide.tests.PerformanceTests.test_mouse_move_near_top_of_large_program_is_fast_enough
Creating test database for alias 'default'...
System check identified no issues (1 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 15.562s

OK
```

Great it passed! Now all of our tests are passing.

So let's try the `mergedeploy` again, using the first few characters of merge commit's hash as our value to "sign off" that all tests did eventually pass:

```
$ git rev-parse HEAD
4dff0746ae59de693b7c5cd3a6550cad47a1e58d

$ python3 manage.py mergedeploy --continue --token=4dff07
Skipping tests because token already available.
Committing the merge...
Deploying...

Fetching latest code from Github...
Fast-forwarding deployed code to target branch...
Fetching latest submodules from Github...
Updating virtual environment...
Checking for deployment issues...
Collecting static files...
Compressing JS and CSS assets...
Building deployment archive...
Applying migrations to database...
Operations to perform:
  Apply all migrations: admin, auth, in_school, ...
Running migrations:
  Applying in_school.0073_auto_20210308_1248... OK
Uploading static files...
  Uploading: CACHE
  Uploading: everything else
Uploading deployment archive to AWS and starting deployment...
Optimizing...
  Clearing expired sessions...
  Auditing user permissions...
  Auditing primary keys...
Deployment STARTED
```

And that's it! A really easy distributed continuous integration system.

### *Related Articles*

* [Tests as Policy Automation](/articles/2021/02/02/tests-as-policy-automation/) - Has ideas for creatively using automated tests to enforce additional (non-functional) properties in your application.
* [Database clamps](/articles/2021/02/09/database-clamps-deterministic-performance-tests-for-database-dependent-code/) - Shows how to write deterministic performance tests for database-dependent code.
