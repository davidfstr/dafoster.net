---
layout: post
title: Copyrights and Licenses for Software
tags: [Software]
x_date_written: 2012-10-23

---

This is a quick overview of copyrights and licenses for software developers who may not know their rights under United States law. I cannot speak for international copyright law.

<div style="padding: .8em 1em .8em; margin-bottom: 1em; border: 1px solid #94da3a;">
    <p style="font-weight: bold; color: #487858;">
        Disclaimer
    </p>
    <p style="margin-bottom: 0em;">
        This article presents legal information but does not provide legal advise. Although all information is correct to the best of my knowledge, I will not be held responsible for the consequences of actions you take based on information found to be incorrect or misleading.
    </p>
</div>


## Copyrights

The first time that a piece of software is published, whether it be in binary or source form, it automatically gains copyright status. This is true even if you don't include the magic words `Copyright (c) 2013 David Foster`.[^magic_words]

[^magic_words]: However if you *do* include the magic words `Copyright (c) 2013 David Foster` it is easier to demonstrate *willful* infringement when you sue someone for infringing your copyright. Willful infringment entitles the copyright owner to higher *damages* (i.e. payments from the infringer) than vanilla infringement.

### Copyright grants the author certain exclusive rights.

That is, other people don't get these rights. Such rights include (but are not limited to):

* The right to *distribute* the software, even for free.
* The right to *sell* the software.

But then you might ask how download sites like Download.com can operate: If by default only the original author has the right to distribute the software they create, a download site would need to get special permission (i.e. a *license*) to distribute most programs on their site, which would be time consuming (and therefore expensive).

In reality, download sites generally rely on software authors to not *enforce* their copyrights. Which brings us to another point:

### Copyrights are useless unless they are enforced.

Enforcement takes the form of the copyright holder actively looking for *infringers*: other people who are distributing or selling the software without permission.

For example, the MPAA may issue a DMCA takedown request to a YouTube user who has (without permission) posted an episode of a TV show that MPAA owns. If the user does not comply with the takedown, the MPAA may sue the user for infringement.

## Licenses

### A copyright holder may waive or share some rights by issuing a *license*.

Licenses may be issued to individuals or companies. For example  a particular distributor may be granted the right to market and sell the software on behalf of the original developer.[^app_store]

For open source software, licenses are typically granted to the community as a whole (i.e. every recipient of the program). This is typically done by including a file called `LICENSE` or `COPYING` with the software. A license may also be found in the software's `README`.

You can write your own custom license (if you feel comfortable writing in legalese). Or you can use one of the more common existing licenses from the community. (See [Common Licenses](#common_licenses) below for a list.)

[^app_store]: If you sell any apps on the App Store, you signed an agreement giving Apple such marketing rights.

### Dual Licensing

Sometimes the same piece of software is offered under multiple licenses.

For example the Qt GUI toolkit has been available under both the GPL license and (with payment) a commercial closed-source license for a long time. Since companies don't like basing their own closed source software on GPL-licensed original software, this gives them an option to use a more corporate-friendly commercial license.

When creating a new piece of software that is based on or uses dual-licensed software, you should document which license the original software is being used under.

If you are the original author of a piece of software, you can issue a new version of the software under additional licenses.

### Changing a Software's License

Under rare circumstances, the license provided with software can change.

As the copyright holder of a piece of software, you may decide to release a new version with a different set of licenses than prior versions. For example you could change the license offered from [BSD](#bsd) to [GPL](#gpl), a rather radical change. Such a change would only be in effect for the newly released version - it would have no effect on older released versions.

If you are not the copyright holder of a piece of software, you cannot change the license(s) under which it is offered.

If there are contributors beyond the original author whose changes have been incorporated into the software, they become partial copyright holders in the software as well unless they explicitly waive their copyright interests via a Contributor Agreeement or similar document. In the event of multiple copyright holders, all holders must agree to any proposed changes in the set of licenses under which the software is offered. Since there may be a large number of contributors (and thus copyright holders), it may be impossible to get permission from everyone, thereby making a license change infeasible.

Projects that are particularly aware of copyright concerns may require all contributors to sign a Contributor Agreement that either waives all copyright interests or explicitly assigns the copyright associated with all contributions to the original author.[^splunk_assignment]

[^splunk_assignment]: For example my present company Splunk requires that all contributors to its open source projects sign a Contributor Agreement of this type.

### No Warranty

All software licenses I have seen explicitly disclaim all warranties. Meaning that if the software harms someone, you can't sue the developer for it. This is great for software developers but in my opinion bad for society.

<a name="common_licenses"></a>
### Common Licenses

Here are the most common open source licenses, arranged generally from most permissive to most restrictive.

If you don't care about the details and only want to know when to use which license, skip to the [summary](#license_summary).

<a name="mit"></a>
#### Public Domain[^pub_domain] <small>&mdash; ultimately permissive</small>

* Do whatever you want with this software.
* This software cannot ever be placed under copyright or any license.

[^pub_domain]: Technically the state of being in the "public domain" is not a license. Any work explicitly released into the public domain is not subject to copyright law at all. In particular there is no copyright holder and can never be a copyright holder in the future.

<a name="mit"></a>
#### MIT License <small>&mdash; super permissive, simple</small>

* Do whatever you want with this software.

<a name="bsd"></a>
#### BSD License <small>&mdash; permissive, simple</small>

* You can redistribute this software.
* (Other rights are not expressedly waived.)
* There are several [variants](http://en.wikipedia.org/w/index.php?title=BSD_licenses&oldid=539421860) of this license.

<a name="apache"></a>
#### Apache 2.0 License <small>&mdash; permissive, complex</small>

* You can do anything normally restricted by copyright.
* You can do anything normally restricted by patent rights.
* Redistribution must be done under certain terms.
* Submissions by contributors automatically fall under
  this license unless specified otherwise.
* You may NOT use trademarks related to this software
  (except in a few special cases).

<a name="lgpl"></a>
#### LGPL License 2.1 <small>&mdash; restrictive, complex</small>

* You can redistribute this software.
* You can modify this software and distribute the derived work. However the derived work must also be LGPL-licensed.
* You can relicense a copy of this software under the GPL. (This is an irreversible action for works derived from the new copy.)
* If you create your own software that uses this LGPL-software, the license of your source code is unaffected. However the resulting *executable* and (sometimes) the *object code* must satisfy the following terms:
    * Modification of the executable and object code is permitted for personal use.
    * Reverse engineering of the executable and object code is permitted.
    * You must give notice that the executable and object code uses this software and that this software is licensed under the LGPL. You must also provide a copy of the LGPL license text.
    * If the software displays copyright notices during its operation (such as in an About box), the LGPL copyright notice for this software must be included and a reference to the full LGPL license text must be provided.
    * Either:
        * (1) Include the source code for this software (including any modifications you made to it) when distributing the executable and object code.
        * (2) Require that the user of the executable or object code have this software installed locally already, and use shared library mechanisms to link the executable against the (unmodified) local copy of this software.
    * If distributing an executable, the nondistributed form of your software must include any data or utility programs necessary to compile the executable.[^include_utility_programs]

[^include_utility_programs]: At face value this doesn't actually seem like a restriction. However the LGPL text cautions, "It may happen that this requirement contradicts the license restrictions of other proprietary libraries that do not normally accompany the operating system. Such a contradiction means you cannot use both them and the Library together in an executable that you distribute."

<a name="gpl"></a>
#### GPL License 2.0 <small>&mdash; restrictive, complex, "viral"</small>

* You can redistribute the source code of this software.
* You can modify this software and distribute the derived work.  However the derived work must also be GPL-licensed.[^gpl_ambiguous_derived]
* You can distribute this software or any software you create based on it, in executable or object code form, provided that you also distribute the corresponding source code (or provide a written offer to do so).

[^gpl_ambiguous_derived]: The GPL is ambiguous with respect to whether a piece of software that you create based on the GPL-licensed software (including merely linking to it) should be considered a derivative work or not. If so, then the GPL is truly "viral": any piece of code that interfaces with GPL-licensed software must also be licensed under the GPL. If not, the GPL still specifies unambiguously that programs based on GPL-licensed software must be distributed with all accompanying source code. Neither proposition is tolerable for most corporate software entities.

#### No License <small>&mdash; ultimately restrictive</small>

* You cannot redistribute or sell this software.
* You cannot create new software that is based on this software (i.e. derivative works).

<a name="license_summary"></a>
### Choosing a License

It is best to pick the license whose terms convey the message you want to send:

* **Public Domain**
    * Do anything you want with this software. It is free forever.
* **MIT**
    * Do anything you want with this software. (Although I might change my mind later.)
* **BSD (4-clause)**
    * Do anything you want with this software, although I want to be attributed (i.e. mentioned as the original author). But I don't want my name used to promote other things.
* **Apache**
    * You can do most things with this software.  
      (And my lawyers want a precise definition of what "most things" means.)
* **LGPL**
    * I want the source code for this software library (and any derived software) to be freely available forever. I also want to enforce that all improvements to this software library that are incorporated into other products be available for independent inspection.
    * I don't care if these extra terms made it burdensome for commercial entities to use my library, although I would like to make it possible for them to still use it if desired.
* **GPL**
    * I want the source code for this software library and any external software that uses it to be freely available forever.
    * I don't care if this means that my software will never be incorporated into a commercial product.
* **Copyright Notice; No License**
    * Don't even think about incorporating this software into another product, or selling it.
* **No Copyright Notice; No License**
    * I don't know about copyright or licenses. Ask me if you want to do something with my software.

Now that I've figured all of this out, it's time to update the licenses I'm using for [my own open source projects](https://github.com/davidfstr?tab=repositories).
