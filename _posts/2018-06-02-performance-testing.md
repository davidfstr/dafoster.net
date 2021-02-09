---
layout: post
title: Performance Testing
tags: [Software, Django]
x_target_audience: [Full-Stack Software Engineers]

---


In this article I will describe the theory of **performance testing**[^perf-testing] and how we conduct such testing in practice at my company TechSmart, in the context of rich web applications and web services.

By the end of this article you should understand how we define performance testing and perhaps get some ideas for implementing or customizing your own tools for performance-testing your own web service.

[^perf-testing]: For the purposes of this article I define performance testing to include **load testing** and **stress testing**.


## Theory

Performance testing of a web service typically involves verifying non-functional requirements such as whether it is:

* **Responsive** - responds quickly to requests
* **Resilient** - handles a large number of requests; avoids crashing outright; rejects or queues requests as needed if too many in progress at once
* **Fault-Tolerant** - whether the service self-heals if it crashes

Performance testing aims to answer the following kinds of questions:

* How responsive is the service under a particular amount of load?  
  (See [§ "perftest run"](#pt-run) below)
* What is the maximum load that the service can handle?  
  (See [§ "perftest maxload"](#pt-maxload) below)
* How responsive is the service under its maximum load?
* What is the bottleneck that is saturated when the service is at its maximum load?  
  (See [§ "Bottleneck isolation"](#bottleneck-isolation) below)
* How does the service behave when stressed beyond its maximum load?  
  (See [§ "Overload behavior"](#overload-behavior) below)

The core of performance testing is **load generation**. You write a program that generates a specified amount of load on your target web service and measure what happens when various amounts of load are applied.

There are many load generation tools that exist:

* One of the oldest load generation tools is [JMeter], which uses a GUI to define simulation programs in an XML-based file format. JMeter uses a separate OS thread for each concurrent HTTP connection which severely limits the number of concurrent HTTP connections it can host on a single box.

* At my company TechSmart we use [Gatling] as our load generation tool. Compared with JMeter, Gatling is far more efficient at generating load because it uses multiplexed async I/O on a single OS thread to handle all HTTP connections. Also, Gatling simulations are written in an actual programming language (Scala) rather than XML, so you can write your simulations with more resilient abstractions and do more-advanced customizations.

[JMeter]: https://jmeter.apache.org/
[Gatling]: http://gatling.io


## Gatling Concepts

### Scenarios and simulations

A **scenario** describes a pattern of HTTP requests that a single user makes against a web service. For example in the `ViewCodePage` scenario a user performs the {`LoginPage.loginWithoutRedirect`, `CodePage.view`} subscenarios which consist of individual HTTP requests.

A **simulation** describes an aggregate pattern of HTTP requests that *multiple* users make against a web service. For example the `ViewCodePage(X, Y)` simulation simulates X users arriving over Y seconds that each perform the actions described in the `ViewCodePage` scenario.

At TechSmart we have written several simulations that exercise each of the major pages on our platform website.


### Simulation parameters

Most simulations written at TechSmart vary their behavior based on *parameters* that are passed in as environment variables. Simulations read these environment variables upon initialization using code like:

```
class LoginAsStudent extends Simulation {
    val X = sys.env.getOrElse("X", "__missing__").toInt
    val Y = sys.env.getOrElse("Y", "__missing__").toInt
```

Thus the set of parameters that a particular simulation expects can be deduced by reading the top of the simulation's source code.

Most simulations at TechSmart support X and Y parameters to inject X users over Y seconds during the simulation.


## Load generation

### The "gatling" management command

The "gatling" management command is a low-level command we've implemented at TechSmart that invokes the Gatling tool, sets up various required paths automatically, and runs a Gatling simulation script.

A typical invocation of the "gatling" management command looks like:

```
$ X=4 Y=1 pm gatling --simulation tskplatform.LoginAsStudent
```

> Note: The `pm` command above is an alias for `python3 manage.py` which is the Django task runner.

This invocation is equivalent to the more-verbose:

```
$ X=4 Y=1 $GATLING_HOME/bin/gatling.sh --simulation tskplatform.LoginAsStudent --simulations-folder $PERFORMANCE_HOME/simulations --data-folder $PERFORMANCE_HOME/data --bodies-folder $PERFORMANCE_HOME/bodies
```

The Gatling tool emits lots of output in the console while it is running and eventually generates an HTML report with detailed statistics about what HTTP requests were made during the simulation, response times for individual and aggregated requests, and other information.

<!-- TODO: Include an image of a typical Gatling report -->


<a name="pt-run"></a>
### The "perftest run" management command

Typically the most important information in the Gatling HTML report generated by running a simulation is the **maximum response time**[^maximum] for a particular type of HTTP request that was made during the simulation. <!-- For example the `ViewCodePage(X, Y)` simulation makes many HTTP requests of type {`view_login`, `submit_login`, and `view_code`} but we only care about the maximum response time of the `view_code` requests. -->

[^maximum]: Many other performance testing tools focus not on the **maximum** response time but rather on other measures such as the **99th percentile** response time or the **mean** response time, which are [inappropriate to use](https://www.youtube.com/watch?v=lJ8ydIuPFeU).

Consequently we've created a "perftest run" management command that behaves similarly to the "gatling" command but automatically presents the maximum response time for the most important request type[^extract-important-request-type] after running the simulation.

[^extract-important-request-type]: The most important request type for a particular simulation is determined by inspecting the source code for a simulation file and looking for a line like `val PROFILED_REQUEST_NAME = "view_code"`.

With the "perftest run" management command, we can easily answer the question:

* How responsive is the service under a particular amount of load?
    - When R requests/second are made continuously, for some R = X/Y:
        - What is the maximum response time?
        - What does the response time distribution look like?

Here is an example of running a simple simulation, using "perftest setup" to create test data and then using "perftest run" to get the maximum response time for a particular amount of load:

```
$ pm perftest setup students 8
Deleting test students...
Creating 8 test student(s)...

$ pm perftest setup calendars 1
Deleting test calendars...
Creating 1 test calendar(s)...
Associating 8 user(s) with 1 calendar(s)...

$ pm perftest run LoginAsStudent 4 1
Running simulation with 4 user(s) over 1 second(s)...
When 4 user(s) over 1 second(s), max response time for request 'submit_login' is 393 ms.
  Report: /Users/me/pkgs/gatling-charts-highcharts-bundle-2.2.2/results/loginasstudent-1497049484195/index.html
```

(We also have a "perftest teardown" command that deletes all test data created by "perftest setup".)

### Targeting remote environments

Our simulations are written by default to target the website running on the developer's local machine (127.0.0.1). For real testing you'll want to run tests on a remote version of the website such as the one on a dedicated perf environment (perf.example.com).

For example, to run a command on our performance environment we would first setup the environment with:

```
$ pm on perf perftest setup students 8
$ pm on perf perftest setup calendars 1
```

> Note: The "on" management command runs some other command in the context of a particular remote environment.

And then we'd run the performance test by typing:

```
$ pm on perf perftest run LoginAsStudent 4 1
```

The "on" command sets the `GATLING_BASE_URL` environment variable (among other things) and the "perftest run" subcommand passes that environment variable to the underlying Gatling simulation. The `GATLING_BASE_URL` variable specifies the base URL that all HTTP requests are prefixed with. For example the above command is equivalent to:

```
$ # (Change environment to "perf", defaulting to its database tier, cache tier, etc)
$ X=4 Y=1 GATLING_BASE_URL=http://perf.example.com pm gatling --simulation tskplatform.LoginAsStudent
```

All simulations support the `GATLING_BASE_URL` parameter to change the base URL because they all use a common Gatling HTTP Protocol object that defines its base URL from `GATLING_BASE_URL`:

```
class LoginAsStudent extends Simulation {
    ...
    val httpProtocol = Common.httpProtocol
    ...
}

object Common {
    private val baseUrl = sys.env.getOrElse(
        "GATLING_BASE_URL", "http://127.0.0.1:8000")
    
    val httpProtocol = http
        .baseURL(baseUrl)
        ...
}
```

## Stress testing

<a name="pt-maxload"></a>
### The "perftest maxload" management command

The "perftest maxload" management command can be used to automatically perform "perftest run" several times to determine the maximum number of users (X) over a given period of time (Y) such that the maximum response time for the HTTP request of interest is less than a particular threshold (1,200 ms by default).

With the "perftest maxload" management command, we can answer the questions:

* What is the maximum load that the service can handle?
    - What is the maximum requests/second that can be made before the requests start backing up and response times go hockeystick?
* How responsive is the service under its maximum load?

An example invocation of "perftest maxload" looks like:

```
$ pm perftest maxload LoginAsStudent --preserve-calendars
Determining baseline response time...

Deleting test students...
Creating 1 test student(s)...
Associating 1 user(s) with 1 calendar(s)...
Running simulation with 1 user(s) over 5 second(s)...
When 1 user(s) over 5 second(s), max response time for request 'submit_login' is 138 ms.
  Report: /Users/davidf/pkgs/gatling-charts-highcharts-bundle-2.2.2/results/loginasstudent-1497567171908/index.html

Seeking shaft of hockeystick...

Deleting test students...
Creating 2 test student(s)...
Associating 2 user(s) with 1 calendar(s)...
Running simulation with 2 user(s) over 5 second(s)...
When 2 user(s) over 5 second(s), max response time for request 'submit_login' is 124 ms.
  Report: /Users/davidf/pkgs/gatling-charts-highcharts-bundle-2.2.2/results/loginasstudent-1497567182571/index.html

(... ditto for 4 users over 5 seconds ... OK ...)
(... ditto for 8 users over 5 seconds ... OK ...)
(... ditto for 16 users over 5 seconds ... OK ...)
(... ditto for 32 users over 5 seconds ... OK ...)
(... ditto for 64 users over 5 seconds ... OK ...)
(... ditto for 128 users over 5 seconds ... FAIL ...)

Seeking knee of hockeystick... About 6 step(s) or 1:41.

Deleting test students...
Creating 96 test student(s)...
Associating 96 user(s) with 1 calendar(s)...
Running simulation with 96 user(s) over 5 second(s)...
When 96 user(s) over 5 second(s), max response time for request 'submit_login' is 3754 ms.
  Report: /Users/davidf/pkgs/gatling-charts-highcharts-bundle-2.2.2/results/loginasstudent-1497567312703/index.html

(... ditto several times, performing a binary search ...)

num_users,response_time,num_seconds
1,138,5
2,124,5
4,120,5
8,157,5
16,123,5
32,182,5
64,920,5
128,6844,5
96,3754,5
80,2407,5
72,1449,5
68,1227,5
66,1232,5
65,939,5

Maximum load is 65 user(s) over 5 second(s) (13.0 users/second) with a response time of 939 ms.
```

Notice how "maxload" used a binary search to automatically find the maximum load that the service could handle before the maximum response times went out of bounds. Neat.

Also notice that "maxload" outputs a CSV of every sample taken. This CSV is useful to graph as a scatterplot to see graphically how the response time varies depending on the number of users. We generate these scatterplot graphs often enough that we'll probably extend "maxload" in the future to just generate a scatterplot image automatically.


<a name="bottleneck-isolation"></a>
### Bottleneck isolation

Once you've determined the maximum load that your service can support, you can ask yourself whether that load is good enough, based on the level of traffic that you forecast your site will receive in the near future.

Should the maximum load not be good enough, you'll want to isolate the **bottleneck** in the system that is constraining the maximum load. Then you can focus on optimizing that bottleneck so that the maximum load increases to be good enough. Note that if you optimize a bottleneck in one area sufficiently, you may find that the bottleneck moves to a different location.

For a web service, the most common bottlenecks in our experience are:

- CPU
    - Is the CPU usage 100% on some box?
- Network
    - Are the number of synchronous database requests made by the application tier to the database tier very high (i.e. more than a dozen or so)?
- Memory
    - Is there no available memory remaining on some box?
    - Is there paging activity on some box?
- IOPS
    - Are the IOPS the maximum for the storage type on some box?

To isolate the bottleneck, use "perftest run" to start generating a load on the service equivalent to the maximum load  it can handle (as measured previously by "perftest maxload") for a long time interval, say 10 minutes. While that load is being generated, use monitoring tools to look at the usage of CPU, Memory, IOPS, and other resources on each box in the system to look for saturation. When you find the saturated resource, that's the bottleneck.

Once you've located the bottleneck, there are usually a few ways to optimize it away. To give you some ideas, here are some bottlenecks that the TechSmart website has hit in its performance testing:

* Not enough frontend workers
    * Saturated resource: All frontend Gunicon workers busy 100% of the time, yet not 100% of the CPU utilized
    * Fix: Reconfigure Gunicorn to increase the worker count to (2*N + 1), where N is the number of CPU cores.
* Too many database requests
    * Saturated resource: Frontends busy waiting on the network for dozens of synchronous database queries to complete for a single page load
    * Fix: Optimize frontend logic to reduce the number of database queries per page load to less than a dozen. Use automated tests to clamp the database query count so that it doesn't increase.
* Not enough frontend CPU
    * Saturated resource: 100% CPU on each box in the frontend cluster.
    * Fix: Increase frontend cluster size from 2 up to 5 boxes. At this point the bottleneck moves elsewhere.

And here are some bottlenecks that our performance testing has identified we will hit under much higher loads than what we currently experience:

* Not enough database CPU
    * Saturated resource: 100% CPU on the single master database server
    * Potential fixes:
        * Cache more aggressively, so that requests are diverted from the database tier to the cache tier.
        * Scale reads. Create read replicas of the database.
        * Scale writes. Shard the database to multiple database masters.
* Not enough database IOPS
    * Saturated resource: IOPS is maximum for the database storage type (i.e. Magnetic or SSD).
    * Potential fixes:
        * Shrink database contents with compression to reduce persisted data volume.
        * Increase RAM on database servers so that the database contents fit into memory, making IOPS irrelevent.
        * Switch database storage type from Magnetic to SSD to increase the maximum IOPS.
        * Scale reads. Create read replicas of the database.
        * Scale writes. Shard the database to multiple database masters.

<a name="overload-behavior"></a>
### Overload behavior

It is useful to determine what happens when your service is subjected to greater than its maximum load. In particular:

- Does it reject requests loudly?
- Does it drop requests silently?
- Does it crash?
- If it crashes, does it automatically restart?

You should decide what desired behavior you want your system to exhibit when receiving a temporary over-maximum load (i.e. a spike) or a sustained over-maximum load (i.e. a flood). Then verify whether the actual behavior matches the desired behavior.

If your service is generally written with infinitely-flexible buffers, it's likely that receiving sustained over-maximum load will causes requests to queue up until memory is exhausted, and the out-of-memory condition will cause the service to crash.

On the other hand if your service is generally written with fixed-size buffers, it's likely that receiving any over-maximum load will cause requests to be rejected or dropped.

## End

Hopefully this article has provided some insight into concepts around performance testing and given you some ideas about how to implement or improve tooling to perform performance testing.

If you have any improvements or other comments on the contents of this article [I'd love to hear from you](/contact).
