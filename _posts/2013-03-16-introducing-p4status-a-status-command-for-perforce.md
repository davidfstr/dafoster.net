---
layout: post
title: "Introducing p4status: A status command for Perforce"
tags: [Software]
x_minor_tags: [Projects]

---

**p4status** works like `git status` (or `svn status`), but works in Perforce.

It will list changelist files and locally modified files that haven't been added to any changelist (including unadded files) in a readable format.

<div style="padding: .8em 1em .8em; margin-bottom: 1em; border: 1px solid #94da3a;">
    <p style="font-weight: bold; color: #487858;">
        Note
    </p>
    <p style="margin-bottom: 0em;">
        The 2012 version of Perforce has an official
        <b>p4 status</b> command. However this command is only available if 
        your corporate Perforce server has been upgraded to 2012. If your 
        company, like mine, has not upgraded their server, this script will 
        make your life easier.
    </p>
</div>

### Example

<pre>
[dfoster ~/dev/p4/mybranch/path/to/myproject]$ p4status
# On changelist 154055
# 
# Changes to be committed in changelist default:
#   (use "p4 revert <file>..." to discard changes in working directory)
# 
#       deleted:    server/apps/setupfx/splunkd/default/extract.conf
# 
# Changes to be committed in changelist 154076:
#   (use "p4 revert <file>..." to discard changes in working directory)
# 
#       new file:   server/apps/setupfx/splunkd/default/inputs-NEW.conf
#       modified:   server/apps/setupfx/splunkd/default/inputs.conf
# 
# Changes not staged for commit:
#   (use "p4 add/edit/delete <file>..." to update what will be committed)
#   (use "p4 sync -f <file>..." to discard changes in working directory)
# 
#       new file:   server/apps/setupfx/splunkd/default/inputs-NEW2.conf
# 
</pre>

### Installation

* Download to your local `bin` directory:
  <https://github.com/davidfstr/dotfiles/blob/master/bin/p4status>
* Mark as executable with `chmod a+x p4status`

### Usage

* `cd` to the primary directory that you'll be working under.
* Run `p4status`.

### Limitations

* Only detects unstaged files under the directory in which the command is run. Therefore it is best to reserve a terminal window that is `cd`-ed to the correct place where this command can be run safely.

* This command is too slow to run from the root of very large branches.

### Alternatives

* Use the excellent Git-to-Perforce bridge, [git-p4].
    * This allows you to work with your Perforce repository as if it were a Git repository. And you can use Git's very fast `git status` command.
* Convince your Perforce server administrator to upgrade to the 2012 version. This may take some time, depending on the size of your company.

### *Related Projects*

* [dotfiles](https://github.com/davidfstr/dotfiles)
    * *My command-line shortcuts, including several for working with Git, particularly in an OS X environment.*


[git-p4]: http://git-scm.com/docs/git-p4