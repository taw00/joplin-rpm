# Joplin - a free and secure notebook application

_.&nbsp;.&nbsp;.&nbsp;packaged for the Fedora, Red Hat (IBM), and OpenSUSE families of linux distributions_

Joplin is a powerful desktop and mobile application for writing and organizing
[markdown-formatted](https://joplinapp.org/markdown/) documents synced
between devices and storeed fully end-to-end encrypted on the local filesystem
as well as the cloud. Joplin can manage large numbers of notes and documents
organised into notebooks. The notes are searchable, can be copied, tagged and
modified either from the applications directly or from your own favorite text
or markdown editor.

You can read more about what Joplin is [here](https://joplinapp.org/) and
[here](https://github.com/laurent22/joplin) and the Joplin forums
[here](https://discourse.joplinapp.org/).

## TL;DR - I want to install Joplin!

Open up a terminal and copy and paste these commands on the commandline of your
Fedora Linux workstation or desktop. Note, I assume you are logged in as a user
that has "sudo" rights.

**For Fedora and EL8 (RHEL8/CentOS8) users . . .**  

_Note that building for RHEL/CentOS has been problematic in the past. I
recommend you migrate your desktop to Fedora._

```
# Initial install...
sudo dnf copr enable taw/joplin
sudo dnf install -y joplin
```
```
# Update/upgrade...
sudo dnf upgrade -y joplin
```

**For OpenSUSE users . . .**

```
# OpenSUSE Leap 15.2
sudo zypper addrepo https://download.copr.fedorainfracloud.org/results/taw/joplin/opensuse-leap-15.2-x86_64/
sudo zypper refresh
sudo zypper install joplin
```

```
# OpenSUSE Tumbleweed
sudo zypper addrepo https://download.copr.fedorainfracloud.org/results/taw/joplin/opensuse-tumbleweed-$basearch/
sudo zypper refresh
sudo zypper install joplin
```

<!--
**For EL7 (RHEL7 and CentOS7) users...**
_note: EL7 builds will be ending soon, migrate to Fedora_

```
# Initial install...
sudo yum install -y yum-plugin-copr
sudo yum copr enable taw/joplin
sudo yum install -y joplin
```
```
# Update/upgrade...
sudo yum update -y joplin
```
-->

Once installed, find Joplin in your menus or normal application search. Enjoy!

* Useful tidbit: all data is mirrored here locally by default (even if you sync to the cloud): `~/.config/Joplin`
* More help can be found at the official Joplin [website](https://joplinapp.org/) and [user forums](https://discourse.joplinapp.org/).

---

# What's in this Github repository?

This repository provides and maintains source packages that can be built to run
on Fedora Linux 29+ and EL8 (testing-only) on x86_64. Binary (fully functional)
application packages based on these source packages are available elsewhere (in
the Fedora Project's COPR repositories) (see below) and make Joplin relatively
easy to install and maintain.

In order to use this application, you only need to download and install the
`joplin` application (via the COPR repos). It will, by default, only store your
notes and documents locally. And unencrypted. It is highly recommended that (a)
you secure your notes with encryption, and (b) configure the application to
sync to the cloud (Dropbox, Nextcloud, etc).

## Why github for this sort of thing?

I build RPM packages for various projects. Constructing and maintaining source
RPMs is very much like any other software or documentation effort. That effort
for Joplin is maintained with source-control via github. Binaries are provided
[here](https://copr.fedorainfracloud.org/coprs/taw/joplin/). But you don't need
to know a whole lot about Fedora's COPR build environment to install and user
these RPMs. Just follow the "TL;DR" instructions below to install Joplin.

If you are technically savvy, you can build your own binary packages from the
source RPMs provided in this github repository. All `src.rpm` files (found here
in Github) will be signed with my general-purpose GPG key found here:
<https://keybase.io/toddwarner/key.asc>.

Packages delivered via COPR are signed with a GPG key specific to that
repository. COPR enablement as shown elsewhere (TL;DR) will install this key
appropriately when necessary.

---

## Comments? Suggestions?
Open an issue here, or send me a note via Keybase -- https://keybase.io/toddwarner

