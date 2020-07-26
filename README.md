# Joplin - a free and secure notebook application

_.&nbsp;.&nbsp;.&nbsp;packaged for the Fedora, Red Hat (IBM), and OpenSUSE families of linux distributions_

Joplin is a powerful desktop and mobile application for writing and organizing
[markdown-formatted](https://joplinapp.org/markdown/) documents synced
between devices and storeed fully end-to-end encrypted on the local filesystem
as well as the cloud. Joplin can manage large numbers of notes and documents
organised into notebooks. The notes are searchable, can be copied, tagged and
modified either from the applications directly or from your own favorite text
or markdown editor.

Notes can be imported from Evernote, to include all associated resources
(images, attachments, etc) and all metadata (geo-location, update time,
creation time, etc). Notes can, of course, also be imported from any other
markdown source.

Mirroring and redundancy between your devices is achieved by a simple, and
optionally encrypted, synchronization with one of the major cloud services
including Nextcloud, Dropbox, Onedrive, WebDAV, or your local or
network-accessible file system.

**More information about Joplin** the project can be found at [joplinapp.org](https://joplinapp.org/) and at it's [GitHub page](https://github.com/laurent22/joplin). **I maintain all RPM package development bits here:** <https://github.com/taw00/joplin-rpm>.

**I can be messaged** at <a href="mailto:t0dd@protonmail.com">t0dd@protonmail.com</a> or as user t0dd in the [Joplin Community Forums](https://discourse.joplinapp.org/).

### OS Notes
* ***Fedora users:*** _Last build for Fedora 30 was Joplin v1.0.224. Upgrade to a newer version of Fedora._
* ***RHEL and CentOS users:*** _Last build for EL7 was Joplin v1.0.216. Building for RHEL/CentOS (any version) has been challenging. How long I can keep it up, I don't know. Migrate to a desktop OS please: i.e., Fedora._
* ***OpenSUSE users:*** _Building for SUSE (any version) has been challenging, for Leap versions in particular. How long I can keep it up is anyone's guess. Just fair warning. Keep up with current releases of OpenSUSE on your desktop._


## TL;DR - I want to install Joplin!

Open up a terminal and copy and paste these commands on the commandline of your
Fedora Linux workstation or desktop. Note, I assume you are logged in as a user
that has "sudo" rights.

**Fedora and RHEL/CentOS users . . .**  

Prep the repository . . .
```
sudo dnf install -y dnf-plugins-core distribution-gpg-keys
sudo dnf copr enable taw/joplin
```

Install Joplin . . .
```
sudo dnf install -y joplin
```

**OpenSUSE users . . .**

Prep the repository . . .

```
# Repository setup for OpenSUSE Leap 15.1
sudo wget https://copr.fedorainfracloud.org/coprs/taw/joplin/repo/opensuse-leap-15.1/taw-joplin-opensuse-leap-15.1.repo -O /etc/zypp/repos.d/taw-joplin-opensuse-leap-15.1.repo
sudo zypper refresh
```
```
# Repository setup for OpenSUSE Leap 15.2
sudo wget https://copr.fedorainfracloud.org/coprs/taw/joplin/repo/opensuse-leap-15.2/taw-joplin-opensuse-leap-15.2.repo -O /etc/zypp/repos.d/taw-joplin-opensuse-leap-15.2.repo
sudo zypper refresh
```
```
# Repository setup for OpenSUSE Tumbleweed
sudo wget https://copr.fedorainfracloud.org/coprs/taw/joplin/repo/opensuse-leap-tumbleweed/taw-joplin-opensuse-leap-tumbleweed.repo -O /etc/zypp/repos.d/taw-joplin-opensuse-leap-tumbleweed.repo
sudo zypper refresh
```

Install Joplin . . .
```
# Install Joplin on OpenSUSE
sudo zypper install joplin
```

Once installed, find Joplin in your desktop menus or do a normal application search. Then run
it. Visit [joplinapp.org](https://joplinapp.org/) for documentation and help.

Useful tidbit:
* application state is maintained at `~/.config/Joplin`
* all Joplin documents and such are mirror locally at `~/.config/joplin-desktop`

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

