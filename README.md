# Joplin: a free and secure notebook - for Fedora Linux

Joplin is a nifty desktop and mobile application for writing and organizing
[markdown](https://en.wikipedia.org/wiki/Markdown)-formatted documents and then
storing them, fully encrypted, on the local filesystem as well as syncing to
the cloud, thus allowing your multiple devices to maintain the same set of
documents.

You can read more about what Joplin is [here](https://joplin.cozic.net) and
[here](https://github.com/laurent22/joplin).

# What's in this repository?

This repository provides and maintains source packages that can be built to run
on Fedora Linux 29+ and EL7 on x86_64. Binary (fully functional) application
packages based on these source packages are available elsewhere (see below) and
make Joplin relatively easy to install and maintain.

In order to use this application, you only need to download and install the
`joplin` application. It will, by default, only store your notes and documents
local. And unencrypted. It is highly recommended that (a) you secure your notes
with encryption, and (b) configure the application to sync to the cloud
(Dropbox, Nextcloud, the).

## Why github for this sort of thing?

I build RPM packages for various projects. Constructing and maintaining source
RPMs is very much like any other software or documentation effort. That effort
for Joplin is maintained with source-control via github. Binaries are provided
[here](https://copr.fedorainfracloud.org/coprs/taw/joplin/). But you don't need
to know a whole lot about Fedora's COPR build environment to install and user
these RPMs. Just follow the "TL;DR" instructions below to install Turtl.

If you are technically able, you can build your own binary packages from the
source RPMs provided in this github repository. Please note that all `src.rpm`
files (found here) will be signed with my general-purpose GPG key found here:
<https://keybase.io/toddwarner/key.asc>.

Packages delivered via COPR are signed with a GPG key specific to that
repository. COPR enablement as shown below (TL;DR) will install this key
appropriately when necessary.

## TL;DR - I want to install Joplin!

Open up a terminal and copy and paste these commands on the commandline of your
Fedora Linux workstation/desktop. Note, I assume you are logged in as a user
that has "sudo" rights.

**For Fedora and EL8 (RHEL8 and CentOS8) users...**
```
# Initial install...
sudo dnf copr enable taw/joplin
sudo dnf install -y joplin
```
```
# Update/upgrade...
sudo dnf upgrade -y joplin
```

**For EL7 (RHEL7 and CentOS7) users...**

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

Once installed, find Joplin in your menus or normal application search and run
it.

* Note: data is, by default, located here: `~/.config/Joplin

## A comment about how Turtl Desktop word-wraps paragraphs of text

**A soft break:** When line breaks in a paragraph of text are ignored upon
rendering the final published content. The markdown interpreter will freely flow the
paragraph of text as needed to fit the dimensions of the document. Hard breaks
can still be forced with <br/> or a double-space at the end of a line.
Traditional markdown assumes 'soft breaking' behavior.

**A hard break:** When every line break in a paragraph of text is treated as a
carriage return in the final published content, regardless of the dimensions
and margin spacing of the output medium.

***Joplin has 'hard breaking' behavior set by default. And as of yet, there is
no easy way to change this.***

You can read more about a "soft line-breaks", otherwise known as a "soft
breaks" or "soft returns" here:
<https://en.wikipedia.org/wiki/Line_wrap_and_word_wrap#Soft_and_hard_returns>

---

## Comments? Suggestions?
Open an issue here, or send me a note via Keybase -- https://keybase.io/toddwarner

## Turtl, that other notebook application

I also build packages for Turtl. Another encrypted multi-device opensource
notebook application. You can find more information about that
[here](https://github.com/taw00/turtl-rpm).

The two projects overlap in functionality, but Turtl is more geared for the
Google Keep-like user experience whereas Joplin aims more at the Evernote use
case.  Joplin has more robust editing features, which make it more useful for
lengthier documents, while Turtl's interface is optimized for shorter notes and
a postit-note feel. Turtl has a more powerful security model and enables
sharing of documents making it very collaborative.

Both are great projects. And yes, there are a lot of great markdown
notebook-ish applications out there. But Turtl and Joplin are my two favorite
projects in this application space.

