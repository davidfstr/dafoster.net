---
layout: post
title: OS Abstractions are Failing Us
tags: [Software]
---

In recent years I've increasingly noticed software being written that cannot get the performance it needs unless it bypasses usual operating system services.

## Concurrency

For example let's consider a program that wants to do many tasks at the same time. Traditionally you would either create multiple **threads** or multiple **processes** for each parallel line of execution. But threads and processes have a lot of overhead - in particular they take up a lot of memory - so it's unwise to have more than a few hundred of them. So if you have a web service handling hundreds or thousands of connections per second, you cannot effectively serve all those requests on one machine using a thread or process per connection.

So some developers turn to writing their web servers with asynchronous I/O and **green threads** so that they can multiplex multiple concurrent tasks onto a single OS thread. You can run millions of these green threads concurrently per machine on modern hardware. That's pretty slick, at least until one of those green threads starts hogging the CPU or accidentally performs a blocking operation. Such a misbehaving green thread will block all other green threads from running, since they use cooperative multitasking and cannot be preempted.

Other developers turn to **microthreads** in languages like Go, Erlang, or Elixir[^elixir]. These environments have an in-process scheduler that multiplexes microthreads onto a single OS thread. Again you can run millions of microthreads concurrently on modern hardware. Happily microthreads *can* be preempted by the scheduler and so a misbehaving microthread won't interfere with other microthreads, although it may cause your server to burn CPU wastefully.

## Disk I/O throughput

These days our disks are solid-state drives with access times similar to RAM rather than the slower rotating magnetic platters of earlier years. Yet my understanding is that the common filesystem and socket abstractions require per-operation overhead comparable to the time spent actually performing the I/O. Yikes. Research seems to be underway considering ways to bypass various OS abstractions to get faster results.[^io_faster_cpu]

## Exciting times

It's neat to be working in computing at the time when some of the fundamental abstractions are being called into question. When practitioners are receptive to change there's an opportunity to contribute new ideas and actually have them tried and used.


[^elixir]: [The Soul of Erlang and Elixir - Saša Jurić](https://youtu.be/JvBT4XBdoUE?t=358)

[^io_faster_cpu]: [I/O Is Faster Than the CPU – Let's Partition Resources and Eliminate (Most) OS Abstractions](https://penberg.org/parakernel-hotos19.pdf)

