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
# Repository setup for OpenSUSE Leap 15.3
sudo wget https://copr.fedorainfracloud.org/coprs/taw/joplin/repo/opensuse-leap-15.3/taw-joplin-opensuse-leap-15.3.repo -O /etc/zypp/repos.d/taw-joplin-opensuse-leap-15.3.repo
sudo zypper refresh
```
```
# Repository setup for OpenSUSE Tumbleweed
sudo wget https://copr.fedorainfracloud.org/coprs/taw/joplin/repo/opensuse-tumbleweed/taw-joplin-opensuse-tumbleweed.repo -O /etc/zypp/repos.d/taw-joplin-opensuse-tumbleweed.repo
sudo zypper refresh
```

Install Joplin . . .
```
# Install Joplin on OpenSUSE
sudo zypper install joplin
```

**All users . . .**

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

### OS Notes

As of version 2.3.3, the normal build process is breaking due to some bizarre
dependency calling python2 in the build tree. Thus far, after many many hours
attempting to work around the issue, I have not been successful in mitigating
the problem. For the foreseeable future, I will be packaging upstream AppImage
binaries until this is resolved.

As of version 2.4.z, I will be moving builds away from EL8 proper and to CentOS Stream only.

<!--
I had to make upstream nodejs available to CentOS, EL7
and EL8, and Fedora (all RedHat/IBM products) to enable binary builds. This is
insecure and wrong, but it is what I have been forced to do. The REPO URLs are
as follows:
- CentOS and EL: https://rpm.nodesource.com/pub_16.x/el/$releasever/$basearch
- Fedora: https://rpm.nodesource.com/pub_16.x/el/$releasever/$basearch
-->

---

## Comments? Suggestions?
Open an issue here, or send me a note via Keybase -- https://keybase.io/toddwarner

---

<!--

## The build process for those who are curious

If minor update — e.g., 2.2.6 to 2.2.7

TEST RELEASE

1. Bump the release in `joplin.spec`, but mark it as a test build.
2. Update the release log in contributed `org.joplinapp.joplin.metainfo.xml` file. Reference my contribs [here](SOURCES/joplin-contrib).
3. Rebundle and commit the `joplin-2.2-contrib.tar.gz` to include that updated `.metainfo.xml` file.
4. Upload `.spec` to COPR build system TEST repo, and press a button to build for CentOS, Fedora, and OpenSUSE.
5. Resolve any failures.
6. Test drive Joplin test build on my own machine and some select recruited testers.

PRODUCTION RELEASE

7. Passes testing, then I flip the testing bit to off in the `.spec` file.
8. Upload `.spec` to COPR build system PRODUCTION repo and build to all those platforms (a reduced set though).
9. Wait for any complaints from the community in case I broke something.

For major releases, e.g., 2.2.7 to 2.3.3, I only add more testing and sometimes
hold off spec file revamps for those releases.

-->
