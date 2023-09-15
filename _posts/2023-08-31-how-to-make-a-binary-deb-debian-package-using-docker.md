---
layout: post
title: How to make a binary .deb Debian package using Docker
tags: [Software]

---

The official instructions for making a .deb Debian package[^1] I found to be
rather long-winded and fiddly, so I came up with a hopefully
more-straightforward method of building a .deb package, using Docker.

[^1]: <https://wiki.debian.org/Packaging>

## <a name="deb-anatomy"></a>What's in a binary .deb package?

A binary .deb package is kind of like a .zip file whose contents are unpacked
to `/` during the installation process. For example, a simple .deb package that
installs a `hello` program to `/usr/bin` might have the following
structure:

```console
$ dpkg -c hello_1.0-1_darwin-amd64.deb  # show contents of .deb package
./usr/
./usr/bin/
./usr/bin/hello
```

A .deb package also contains a **control file** with metadata describing the package:

```console
$ cat ./DEBIAN/control
Package: hello
Version: 1.0-1
Section: misc
Priority: optional
Architecture: all
Maintainer: David Foster <david@example.com>
Description: A program that prints a hello world message and exits.
```

## How can Docker be used to build a binary .deb package?

Let's say you make a Dockerfile that builds and installs the `hello` program,
based on the official build and install instructions for the program.
Such a Dockerfile might look like:

```dockerfile
FROM debian:latest

# Install build dependencies
RUN apt-get update
RUN apt-get install build-essential -y  # install gcc

# Download source code
COPY ./hello.c /usr/src/

# Compile the binary (AKA: make)
RUN gcc -o /tmp/hello /usr/src/hello.c

# Install the binary (AKA: make install)
RUN cp /tmp/hello /usr/bin/hello
```

When you build a Docker image from such a Dockerfile, each capitalized
command in the Dockerfile (like `RUN` and `COPY`) creates a separate **layer**
which contains the files created by the command.

Notably, the last `RUN` command above which actually installs the `hello` binary
creates a layer containing *exactly those files which should be installed*.

If we could extract the files from that "install" layer then we'd have exactly
the set of files that a `hello` .deb package should install. It turns out we *can*!

## Extracting the installed files from a Docker image layer

First build the Docker image from the Dockerfile:

```console
$ docker build -t hello-build:latest .
```

Then extract the contents of all Docker image layers:

```console
$ mkdir build
$ docker save -o build/hello-build.tar hello-build:latest
$ cd build
$ tar xf hello-build.tar
```

You should see a directory structure like:

```console
$ tree
.
├── 05bc8a33fbd971aa8c6d6e3613ea41f0477e4507229e6072c43f3ef61b549b82
│   ├── VERSION
│   ├── json
│   └── layer.tar
├── 2745707919ffe930cb00def7c34e4e9bbac8e30b99f66e631edb2eb6b3a5b89c
│   ├── VERSION
│   ├── json
│   └── layer.tar
├── 3bda020d2a872426189c67863e8add029463c14957b9fa17690e591a6a1455e2
│   ├── VERSION
│   ├── json
│   └── layer.tar
├── 440d2890e2b9b3ce91db819ee42fb77a807daf2f46f02579a4c0df9274eebc13
│   ├── VERSION
│   ├── json
│   └── layer.tar
├── 8c7b379494075edb4563162a9e844d548d797a470cb55c3f49f0969b9437b1e4.json
├── 9bc167af8f88fb2b70b47cc2b2be68a8be5862e49572353c13075eb5ce8845bc
│   ├── VERSION
│   ├── json
│   └── layer.tar
├── b6100c2b22f88d1698c24d418c989bfe0174d7a4e20ca7d60824dc36d1013638
│   ├── VERSION
│   ├── json
│   └── layer.tar
├── hello-build.tar
├── manifest.json
└── repositories
```

Each of the directories with a very long name corresponds to a Docker image layer.
The contents of each directory is the set of files the layer contains.

The `manifest.json` contains information about which layer corresponds to
which directory:

```console
$ cat manifest.json | jq
[
  {
    "Config": "8c7b379494075edb4563162a9e844d548d797a470cb55c3f49f0969b9437b1e4.json",
    "RepoTags": [
      "hello-build:latest"
    ],
    "Layers": [
      "05bc8a33fbd971aa8c6d6e3613ea41f0477e4507229e6072c43f3ef61b549b82/layer.tar",
      "b6100c2b22f88d1698c24d418c989bfe0174d7a4e20ca7d60824dc36d1013638/layer.tar",
      "9bc167af8f88fb2b70b47cc2b2be68a8be5862e49572353c13075eb5ce8845bc/layer.tar",
      "440d2890e2b9b3ce91db819ee42fb77a807daf2f46f02579a4c0df9274eebc13/layer.tar",
      "2745707919ffe930cb00def7c34e4e9bbac8e30b99f66e631edb2eb6b3a5b89c/layer.tar",
      "3bda020d2a872426189c67863e8add029463c14957b9fa17690e591a6a1455e2/layer.tar"
    ]
  }
]
```

Now remember, we want to find the files in the layer for the *install* step in the
Dockerfile, which happens to be the last step and thus also the last layer:

```dockerfile
# Install the binary (AKA: make install)
RUN cp /tmp/hello /usr/bin/hello
```

So we just need to look at the last item in the `"Layers"` key from the
`manifest.json` file to find the directory we want:

```
"3bda020d2a872426189c67863e8add029463c14957b9fa17690e591a6a1455e2/layer.tar"
```

So let's unpack the files for that layer:

```console
$ export LAYER_TARFILE="3bda020d2a872426189c67863e8add029463c14957b9fa17690e591a6a1455e2/layer.tar"
$ mkdir layer
$ tar Cxf layer $LAYER_TARFILE
$ cd layer
```

And indeed we see the installed files:

```console
$ tree
.
└── usr
    └── bin
        └── hello
```

## Building a .deb package from a set of files

Remember that a binary .deb package is built from a directory of files to install
*plus* [a `DEBIAN` directory containing at least a `control` file](#deb-anatomy).

### Write a `control` file

Since we already have a directory of files to install from the last step,
we just need to add a `DEBIAN` directory and write a `control` file:

```console
$ mkdir DEBIAN
$ cat > DEBIAN/control <<EOF
Package: hello
Version: 1.0
Section: misc
Priority: optional
Architecture: all
Maintainer: David Foster <david@example.com>
Description: Prints a hello world message and exits.
EOF
```

Here are some important parameters in a typical `control` file:

* **[Package]** (required) -- Name of the package. Used to refer to it as a dependency.
* **[Version]** (required) -- Version of the package.
* **[Section]** (recommended) -- `misc` is fine, although a more targeted category 
  may make your package more discoverable if you upload it to a package archive.
* **[Priority]** (recommended) -- `optional` is probably what you want.
* **[Architecture]** (required) -- `all` disables machine architecture checking.
  Get a list of valid architectures for your current machine using `dpkg-architecture -L`.
* **[Maintainer]** (required) -- The package maintainer’s name and email address.
* **[Description]** (required) -- The short description and long description of the package.
* **[Depends]** -- Names other packages to install alongside this package.
* **[Recommends]** -- Names other packages to install by default alongside this package unless
  `--no-install-recommends` is passed to `apt-get install`.
* **[Conflicts]** -- Names other packages whose presence will prevent this package from
  being installed.

[Package]: https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-package
[Version]: https://www.debian.org/doc/debian-policy/ch-controlfields.html#version
[Section]: https://www.debian.org/doc/debian-policy/ch-archive.html#s-subsections
[Priority]: https://www.debian.org/doc/debian-policy/ch-archive.html#s-priorities
[Architecture]: https://www.debian.org/doc/debian-policy/ch-customized-programs.html#s-arch-spec
[Maintainer]: https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-maintainer
[Description]: https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-description
[Depends]: https://www.debian.org/doc/debian-policy/ch-relationships.html#s-binarydeps
[Recommends]: https://www.debian.org/doc/debian-policy/ch-relationships.html#s-binarydeps
[Conflicts]: https://www.debian.org/doc/debian-policy/ch-relationships.html#s-conflicts

### Build the `.deb`

With the `control` file written, we now have all files that we want to put into
the `.deb` package. So let's actually bundle it into a `.deb`:

```console
$ docker run -it -v .:/home --name deb-builder debian:latest
$$ dpkg-deb --root-owner-group --build home
```

### Inspect the `.deb`

You can inspect the contents of the `.deb` to verify that it looks reasonable:

```console
$$ dpkg -c home.deb | more  # (Optional) verify contents look OK
drwxr-xr-x root/root         0 2023-09-08 18:50 ./
drwxr-xr-x root/root         0 2023-07-25 00:00 ./usr/
drwxr-xr-x root/root         0 2023-09-08 18:46 ./usr/bin/
-rwxr-xr-x root/root     15952 2023-09-08 18:46 ./usr/bin/hello
```

### Find and fix errors with Lintian

You can also use the Lintian tool to look for problems with your package:

```console
$$ apt-get update && apt-get install lintian -y
$$ lintian --tag-display-limit 0 home.deb  # (Optional) verify output looks OK; some ERRs are OK
E: hello: arch-independent-package-contains-binary-or-object [usr/bin/hello]
E: hello: extended-description-is-empty
E: hello: no-changelog usr/share/doc/hello/changelog.gz (native package)
E: hello: no-copyright-file
E: hello: unstripped-binary-or-object [usr/bin/hello]
W: hello: no-manual-page [usr/bin/hello]
W: hello: undeclared-elf-prerequisites (libc.so.6) [usr/bin/hello]
```

Each line starting with `E` is an **error**, and each line starting with `W` is a **warning**.

You can get a detailed description of each error by adding running lintian
with the `-i` option:

```console
$$ lintian -i --tag-display-limit 0 home.deb
E: hello: arch-independent-package-contains-binary-or-object [usr/bin/hello]
N: 
N:   The package contains a binary or object file but is tagged Architecture: all.
N:   
N:   If this package contains binaries or objects for cross-compiling or binary blobs for other purposes independent of the
N:   host architecture (such as BIOS updates or firmware), please add a Lintian override.
N: 
N:   Visibility: error
N:   Show-Always: no
N:   Check: binaries/architecture
...
```

It's quite possible the .deb may work as-is even if there are errors.
However it's best to fix as many of the errors and warnings as possible.

For example, to fix the following error:

```
W: hello: undeclared-elf-prerequisites (libc.so.6) [usr/bin/hello]
```

You can add `Depends: libc6` to the `control` file.

### Don't install to `/usr/local`!

A common type of error you *do* need to fix happens when you try to install 
something into `/usr/local`, because Debian reserves the `local` directory
for its own purposes. For example if we installed `hello` to `/usr/local`,
we'd see Lintian errors that look like:

```
E: hello: dir-in-usr-local [usr/local/bin/]
E: hello: file-in-usr-local [usr/local/bin/hello]
```

Fix those errors by altering the build process in your Dockerfile to install to
`/usr/bin` rather than to `/usr/local/bin`. For many Linux programs built 
using a line like `./configure`, you can usually alter that line to be 
`./configure --prefix=/usr` to configure the install process to install to 
`/usr/bin`.

### Copy out the `.deb`

Once you're happy with the `.deb` package, copy it out of your build container,
give it a proper name, and exit the build container:

```console
$$ cp home.deb /home/hello_1.0_all.deb
$$ exit
$ ls
hello_1.0_all.deb
...
```

> If you need to reenter the build container later, use:
> ```console
> $ docker start -i deb-builder
> ```

### Testing your .deb package

It's a good idea to verify that package is installable.
You can do that in another fresh container:

```console
$ docker run -it -v .:/home --name deb-tester debian:latest
$$ apt-get update
$$ apt-get install ./home/hello_1.0_all.deb -y
$$ which hello  # ensure installed
/usr/bin/hello
$$ hello  # ensure runs
Hello world!
$$ exit
```

> If you need to reenter the testing container later, use:
> ```console
> $ docker start -i deb-tester
> ```

## Putting it all together

A complete example of all the files to build the `hello` .deb package
is in the following GitHub repository:

* [hello-deb-package](https://github.com/davidfstr/hello-deb-package#readme)

<!--
And here is a real-world example of creating a .deb package to install 
Python 2.7 in Debian 12 Bookworm:

TODO
-->

