# joplin.spec
# vim:tw=0:ts=2:sw=2:et:
#
# Joplin - A secure notebook application.
#          End-to-end encrypted markdown. Syncable between your devices.
#
# The RPM builds...
# https://github/taw00/joplin-rpm
# https://copr.fedorainfracloud.org/coprs/taw/joplin
#
# The upstream project...
# https://joplin.cozic.net/
# https://github.com/laurent22/joplin

# ---

# Package (RPM) name-version-release.
# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]

# Filters out unneccessary provides
%{?nodejs_default_filter}

Name: joplin
Summary: A free and secure notebook application

%define appid org.joplinapp.joplin

%define name_cli joplin-cli
%define name_desktop joplin-desktop

%define targetIsProduction 1
%define nativebuild 1

# Only used if the dev team or the RPM builder includes things like rc3 or the
# date in the source filename
%define buildQualifier 20190226
%undefine buildQualifier

# VERSION
%define vermajor 2.0
%define verminor 11
Version: %{vermajor}.%{verminor}

# RELEASE
%define _pkgrel 2
%if ! %{targetIsProduction}
  %define _pkgrel 1.1
%endif

# MINORBUMP
%define minorbump taw

#
# Build the release string - don't edit this
#

%define snapinfo highlyexperimental
%if %{targetIsProduction}
  %undefine snapinfo
%else
  %define snapinfo testing
%endif
%if 0%{?buildQualifier:1}
  %define snapinfo %{buildQualifier}
%endif

# pkgrel will also be defined, snapinfo and minorbump may not be
%define _release %{_pkgrel}
%if 0%{?snapinfo:1}
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}
  %endif
%else
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}%{?dist}
  %endif
%endif

Release: %{_release}
# ----------- end of release building section

# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing
# Apache Software License 2.0
License: MIT
# URL: https://joplin.cozic.net/
URL: https://joplinapp.org/

# Note1, for example, this will not build on ppc64le
# Note2, attempted aarch64 (also called arm64?). Thus far, the builds fail.
#ExclusiveArch: x86_64 i686 i586 i386 aarch64
ExclusiveArch: x86_64

# how are debug info and build_ids managed (I only halfway understand this):
# https://github.com/rpm-software-management/rpm/blob/master/macros.in
# ...flip-flop next two lines in order to disable (nil) or enable (1) debuginfo package build
%define debug_package 1
%define debug_package %{nil}
%define _unique_build_ids 1
%define _build_id_links alldebug

# https://fedoraproject.org/wiki/Changes/Harden_All_Packages
# https://fedoraproject.org/wiki/Packaging:Guidelines#PIE
%define _hardened_build 1

# https://fedoraproject.org/wiki/Packaging:SourceURL
#%%define sourceroot %%{name}-%%{vermajor}-%%{buildQualifier}
%define sourceroot %{name}-%{vermajor}
%define sourcetree %{name}-%{version}
%define sourcetree_contrib %{name}-%{vermajor}-contrib
# /usr/share/joplin
%define installtree %{_datadir}/%{appid}

Source0: https://github.com/laurent22/joplin/archive/v%{version}/%{sourcetree}.tar.gz
Source1: https://github.com/taw00/joplin-rpm/raw/master/SOURCES/%{sourcetree_contrib}.tar.gz

# See https://discourse.joplinapp.org/t/dependency-on-canberra/6696
Requires: libcanberra-gtk2 libnotify
Requires: libnotify

# Exclusions from provides and requires calculations and from the results
#%%global __provides_exclude_from ^(.%%{installtree}/.*\\.so.*|%%{installtree}/cli/node_modules/.*|%%{installtree}/cli/build/.*|%%{installtree}/cli/tests/.*|%%{installtree}/desktop/resources/.*)$
#%%global __requires_exclude_from ^(.%%{installtree}/.*\\.so.*|%%{installtree}/cli/node_modules/.*|%%{installtree}/cli/build/.*|%%{installtree}/cli/tests/.*|%%{installtree}/desktop/resources/.*)$
%global __provides_exclude_from ^(.%{installtree}/.*\\.so.*|%{installtree}/desktop/resources/node_modules/.*|%{installtree}/desktop/resources/app.asar.unpacked/node_modules/.*)$
%global __requires_exclude_from ^(.%{installtree}/.*\\.so.*|%{installtree}/desktop/resources/node_modules/.*|%{installtree}/desktop/resources/app.asar.unpacked/node_modules/.*)$
%global __provides_exclude ^(lib.*\\.so.*)$
%global __requires_exclude ^((libffmpeg[.]so.*)|(lib.*\\.so.*)|(/usr/bin.*/coffee))$

BuildRequires: libsecret-devel
BuildRequires: git rsync findutils grep
BuildRequires: desktop-file-utils
# provided by coreutils RPM
#BuildRequires: /usr/bin/readlink /usr/bin/dirname

# OPENSUSE
%if 0%{?suse_version:1}
BuildRequires: ca-certificates-cacert ca-certificates-mozilla ca-certificates
BuildRequires: appstream-glib
BuildRequires: gcc-c++
# this is ugly and wrong. but it works.
BuildRequires: /usr/bin/python
# Leap
%if 0%{?sle_version}
# Leap 15.1
%if 0%{?sle_version} == 150100
BuildRequires: nodejs12 npm12 nodejs12-devel nodejs-common
%endif
# Leap 15.2
%if 0%{?sle_version} == 150200
#BuildRequires: nodejs12 npm12 nodejs12-devel nodejs-common
#BuildRequires: nodejs14 npm14 nodejs14-devel nodejs-common
BuildRequires: nodejs npm nodejs-devel nodejs-common
%endif
# Tumbleweed
%else
#BuildRequires: nodejs10 npm10 nodejs10-devel nodejs-common
#BuildRequires: nodejs14 npm14 nodejs14-devel nodejs-common
#BuildRequires: nodejs16 npm16 nodejs16-devel nodejs-common
BuildRequires: nodejs npm nodejs-devel nodejs-common
%endif
%endif

# CENTOS / RHEL
# EL7 is too far behind on its available nodejs. Therefore we pull
# from upstream for the build. Add this repos to mock and COPR.
#     https://rpm.nodesource.com/pub_10.x/el/$releasever/$basearch
#     In the past, this repo was also included: https://dl.yarnpkg.com/rpm/
# EL8's default nodejs is v10. We need v12 which is provided in the nodejs 12
# module. You have to enable the module in COPR in the settings for
# EL8: nodejs:12
# This is the equivalent of doing sudo dnf module enable nodejs:12 at the
# commandline. I do not know a way of specifying this in the .spec file.
%if 0%{?rhel:1}
BuildRequires: gcc-c++
BuildRequires: libappstream-glib

# EL7
%if 0%{?rhel} == 7
BuildRequires: python
BuildRequires: nodejs >= 2:10

# EL8
%else
%if 0%{?rhel} == 8
BuildRequires: python3
BuildRequires: nodejs npm

# EL9 (which doesn't exist yet)
%else
BuildRequires: python
BuildRequires: nodejs npm

%endif
%endif
%endif

# FEDORA
%if 0%{?fedora:1}
BuildRequires: libappstream-glib
BuildRequires: gcc-c++
BuildRequires: python
BuildRequires: nodejs npm
%endif

#t0dd: I often add these extra packages to enable mock environment introspection
%if ! %{targetIsProduction}
#BuildRequires: tree vim-enhanced less dnf iputils findutils
BuildRequires: tree vim-enhanced less dnf iputils
%endif


%description
Joplin is a secure notebook application designed to organize your notes,
to-dos, web-snippets, and more. Documents are organized using tags and
hierarchical notebooks and can be end-to-end synchronized with all your
devices. Notes are can be searched, copied, tagged, and modified either from
the applications directly or from your own favorite text editor. Notes are
composed in the ever-popular and familiar markdown format.

Notes can, of course, be imported from any markdown source Notes can also be
imported from Evernote. Import from Evernote includes all associated resources
(images, attachments, etc) and all metadata (geo-location, update time,
creation time, etc). Notes can, of course, also be imported from any other
markdown source.

Mirroring to your devices and redundancy is achieved by a simple—and
optionally end-to-end encrypted—synchronization to various cloud services
including Nextcloud, Dropbox, Onedrive, WebDAV, or your local or
network-accessible file system.


%prep
# Prep section starts us in directory {_builddir}

echo "======== prep stage ========"

rm -rf %{sourceroot} ; mkdir -p %{sourceroot}

# OPENSUSE
# The prep section is the first place we can run shell commands. Therefore,
# these checks are here...
%if 0%{?suse_version:1}
  echo "======== OpenSUSE version: %{suse_version} %{sle_version}"
  echo "-------- Leap 15.1  will report as 1500 150100"
  echo "-------- Leap 15.2  will report as 1500 150200"
  echo "-------- Tumbleweed will report as 1550 undefined"
  %if 0%{?sle_version} && 0%{?sle_version} < 150100
    echo "Builds for OpenSUSE Leap older than 15.1 are not supported."
    exit 1
  %endif
%endif

# FEDORA
%if 0%{?fedora:1}
  echo "======== Fedora version: %{fedora}"
  %if 0%{?fedora} <= 29
    echo "Builds for Fedora 29 and older are no longer supported."
    exit 1
  %endif
%endif

# CENTOS / RHEL (EL7 and EL8)
%if 0%{?rhel:1}
  echo "======== EL version: %{rhel}"
  %if 0%{?rhel} < 7
    echo "Builds for EL 6 and older are not supported."
    exit 1
  %endif
  %if 0%{?rhel} == 8
    # In order to build the SQLite bits, a version of python must be addressable as
    # python from the commandline. Python3 on EL8 is addessed as /usr/bin/python3.
    # Python got  bit crazy, but is settling down with the end of python2 as of
    # January 2020. Read more about python and how it is packaged here:
    # https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/
    mkdir -p $HOME/.local/bin
    if [ ! -e "$HOME/.local/bin/python" ] ;  then
      ln -s /usr/bin/python3 $HOME/.local/bin/python
    fi
  %endif
%endif

# Unarchived source tree structure (extracted in {_builddir})
#   sourceroot             joplin-1.0
#    \_{sourcetree}          \_joplin-1.0.174
#    \_{sourcetree_contrib}  \_joplin-1.0-contrib

# Extract into {_builddir}/{sourceroot}/
# Source0 and Source1
%setup -q -T -D -a 0 -n %{sourceroot}
%setup -q -T -D -a 1 -n %{sourceroot}


# For debugging purposes...
%if ! %{targetIsProduction}
  cd .. ; tree -d -L 2 %{sourceroot} ; cd -
%endif


%build
# Build section starts us in directory {_builddir}/{sourceroot}
echo "======== build stage ========"

cd %{sourcetree}

# FEDORA
%if 0%{?fedora:1}
%if 0%{?fedora} >= 29
%if 0%{?fedora} >= 33
%endif
# Fedora 28 or older
%else
  # NOTE: This is here for posterity.
  #       We are no longer building for Fedora 28 and older and I don't think
  #       that yarn is used anymore.
  npm install yarn
  _pwd=$(pwd)
  echo "======== Mapping yarn so it can be found in the path"
  mkdir -p $HOME/.local/bin
  if [ ! -e "$HOME/.local/bin/yarn" ] ;  then
    ln -s ${_pwd}/node_modules/.bin/yarn $HOME/.local/bin/yarn
  fi

  yarn add electron-builder --dev
  yarn add electron-packager --dev
%endif
%endif

# CENTOS / RHEL (EL7 and EL8)
%if 0%{?rhel:1}
%if 0%{?rhel} >= 8
#  npm update
#  npm install node-gyp
#  npm install node-pre-gyp
%endif
%endif

echo "
###### NOTE: You may see the build gripe about a husky build failure
######       because a .git can't be found. Ignore it.
"

### BUILD IT!
npm install

# CLI - can't get to work yet, so pulling from the RPM for now
#cd packages/app-cli
#npm run build
#cd ../..
# DESKTOP
cd packages/app-desktop
npm run dist
cd ../..

# experimenting. trying to get rid of all those error messages in the
# developmental console in the UI
#%%if 0%%{?nativebuild:1}
#cd packages
#mkdir app-desktop/dist/linux-unpacked/resources/app.asar.unpacked/node_modules/\@joplin
#cp -a lib app-desktop/dist/linux-unpacked/resources/app.asar.unpacked/node_modules/\@joplin/
#cd ..
#%%endif

### CLEANUP
%if 0%{?nativebuild:1}
cd packages/app-desktop/dist/linux-unpacked/resources
# 7zip-bin and wrong architectures
# For whatever reason, we end up with several 7zip-bin architectures. They
# trigger incorrect and unmeetable dependencies. So we strip out the irrelevant
# ones.
# Question: Do we even need 7zip-bin at all? Probably(?), so leaving it in.
%ifarch x86_64 amd64 aarch64
rm -rf $(find app*/node_modules/7zip-bin-linux/* -type d | grep -v x64)
%else
rm -rf $(find app*/node_modules/7zip-bin-linux/* -type d | grep -v ia32)
%endif
cd ../../../../..
%endif


%install
# Install section starts us in directory {_builddir}/{sourceroot}

# Cheatsheet for some built-in RPM macros:
# https://fedoraproject.org/wiki/Packaging:RPMMacros
#   _builddir = {_topdir}/BUILD
#   _buildrootdir = {_topdir}/BUILDROOT
#   buildroot = {_buildrootdir}/{name}-{version}-{release}.{_arch}
#   _datadir = /usr/share
#   _mandir = /usr/share/man
#   _sysconfdir = /etc
#   _libdir = /usr/lib or /usr/lib64 (depending on system)
#   _metainfodir = /usr/share/metainfo
#  Note: We install to /usr/share/ because /opt is for unpackaged applications
#        http://www.pathname.com/fhs/pub/fhs-2.3.html

%if 0%{?suse_version:1}
# Old versions of RPM and opensuse as of Leap 15.2 and Tumbleweed (2020-07)
# don't have _metainfodir defined
%define _metainfodir %{_datadir}/metainfo
%endif

# Create directories
#install -d %%{buildroot}%%{_libdir}/%%{appid}
install -d -m755 -p %{buildroot}%{_bindir}
install -d %{buildroot}%{installtree}/desktop
# CLI: can't get to work at the moment, so pulling from the RPM.
#install -d %%{buildroot}%%{installtree}/cli
install -d %{buildroot}%{_datadir}/applications
install -d %{buildroot}%{_metainfodir}

echo "\
[Desktop Entry]
Type=Application
Name=Joplin
GenericName=Secure Notebook
Comment=A free and secure notebook management application
Exec=%{name_desktop}
Icon=%{appid}
Terminal=false
# https://specifications.freedesktop.org/menu-spec/latest/apa.html
Categories=Network;Office;TextEditor;WordProcessor;X-Markdown;X-KaTeX;X-Mermaid;X-Fountain;X-E2EE;
Keywords=secure;security;privacy;private;notes;bookmarks;collaborate;research;
StartupWMClass=Joplin
StartupNotify=true

# .desktop spec: https://www.freedesktop.org/wiki/Specifications/desktop-entry-spec/
# .metainfo.xml spec: https://www.freedesktop.org/software/appstream/docs/

" > %{buildroot}%{_datadir}/applications/%{appid}.desktop

# icons
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/hicolor-64-%{appid}.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{appid}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/128x128.png               %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{appid}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/256x256.png               %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{appid}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/512x512.png               %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{appid}.png
install -D -m644 -p %{sourcetree}/Assets/JoplinIcon.svg                      %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{appid}.svg

# icons
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/highcontrast-64-%{appid}.png          %{buildroot}%{_datadir}/icons/HighContrast/64x64/apps/%{appid}.png
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/highcontrast-128-%{appid}.png       %{buildroot}%{_datadir}/icons/HighContrast/128x128/apps/%{appid}.png
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/highcontrast-256-%{appid}.png       %{buildroot}%{_datadir}/icons/HighContrast/256x256/apps/%{appid}.png
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/highcontrast-512-%{appid}.png       %{buildroot}%{_datadir}/icons/HighContrast/512x512/apps/%{appid}.png
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/highcontrast-scalable-%{appid}.svg %{buildroot}%{_datadir}/icons/HighContrast/scalable/apps/%{appid}.svg

desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.desktop
install -D -m644 -p %{sourcetree_contrib}/%{appid}.metainfo.xml %{buildroot}%{_metainfodir}/%{appid}.metainfo.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml

# Native build
%if 0%{?nativebuild:1}
# CLI: can't get to work at the moment, so pulling from the RPM. TODO: tackle another day
#cp -a %%{sourcetree}/packages/app-cli/build/* %%{buildroot}%%{installtree}/cli
#ln -s %%{installtree}/cli/main.js %%{buildroot}%%{_bindir}/%%{name_cli}

cp -a %{sourcetree}/packages/app-desktop/dist/linux-unpacked/* %{buildroot}%{installtree}/desktop
mv %{buildroot}%{installtree}/desktop/\@joplinapp-desktop %{buildroot}%{installtree}/desktop/%{name_desktop}
ln -s %{installtree}/desktop/%{name_desktop} %{buildroot}%{_bindir}/%{name_desktop}

# Alternative build: package the AppImage build instead
%else
# This is SUPER ugly... It's an alternative if we want to use it.
install -D -m755 -p %{sourcetree}/packages/app-desktop/dist/'Joplin-'%{version}'.AppImage' %{buildroot}%{_bindir}/%{name_desktop}
%endif


%files
%defattr(-,root,root,-)
%license %{sourcetree}/LICENSE
%doc %{sourcetree}/packages/app-desktop/dist/linux-unpacked/LICENSE.electron.txt
%doc %{sourcetree}/packages/app-desktop/dist/linux-unpacked/LICENSES.chromium.html
# DESKTOP
%{_bindir}/%{name_desktop}
# CLI - not working at the moment, so ... pulled.
#%%{_bindir}/%%{name_cli}
# desktop environment metadata
%{_datadir}/applications/%{appid}.desktop
%{_metainfodir}/%{appid}.metainfo.xml
# desktop environment icons
   %{_datadir}/icons/hicolor/64x64/apps/%{appid}.png
 %{_datadir}/icons/hicolor/128x128/apps/%{appid}.png
 %{_datadir}/icons/hicolor/256x256/apps/%{appid}.png
 %{_datadir}/icons/hicolor/512x512/apps/%{appid}.png
%{_datadir}/icons/hicolor/scalable/apps/%{appid}.svg
   %{_datadir}/icons/HighContrast/64x64/apps/%{appid}.png
 %{_datadir}/icons/HighContrast/128x128/apps/%{appid}.png
 %{_datadir}/icons/HighContrast/256x256/apps/%{appid}.png
 %{_datadir}/icons/HighContrast/512x512/apps/%{appid}.png
%{_datadir}/icons/HighContrast/scalable/apps/%{appid}.svg

%if 0%{?nativebuild:1}
%{installtree}
%endif


%post
umask 007
#/sbin/ldconfig > /dev/null 2>&1
/usr/bin/update-desktop-database &> /dev/null || :


%postun
umask 007
#/sbin/ldconfig > /dev/null 2>&1
/usr/bin/update-desktop-database &> /dev/null || :


%changelog
* Thu Jun 24 2021 Todd Warner <t0dd_at_protonmail.com> 2.0.11-2.taw
* Thu Jun 24 2021 Todd Warner <t0dd_at_protonmail.com> 2.0.11-1.1.testing.taw
  - Fixes https://github.com/laurent22/joplin/issues/4330  
    Apparently, app-desktop/build is not a superfluous build artifact.
  - Updated nodejs versions for OpenSUSE Leap 15.2 and Tumbleweed
  - Added spec macros that cleans up nodejs-triggered provides.

* Wed Jun 16 2021 Todd Warner <t0dd_at_protonmail.com> 2.0.11-1.taw
* Wed Jun 16 2021 Todd Warner <t0dd_at_protonmail.com> 2.0.11-0.1.testing.taw
  - https://github.com/laurent22/joplin/releases/tag/v2.0.11

* Mon May 17 2021 Todd Warner <t0dd_at_protonmail.com> 1.8.5-1.taw
* Mon May 10 2021 Todd Warner <t0dd_at_protonmail.com> 1.8.5-0.1.testing.taw
  - https://github.com/laurent22/joplin/releases/tag/v1.8.5 pre-release
  - Updated OpenSUSE's tumbleweed nodejs BuildRequires

* Thu Feb 4 2021 Todd Warner <t0dd_at_protonmail.com> 1.7.11-1.taw
* Thu Feb 4 2021 Todd Warner <t0dd_at_protonmail.com> 1.7.11-0.1.testing.taw
  - 1.7.11 — https://github.com/laurent22/joplin/releases/tag/v1.7.11

* Fri Jan 22 2021 Todd Warner <t0dd_at_protonmail.com> 1.6.8-1.taw
* Fri Jan 22 2021 Todd Warner <t0dd_at_protonmail.com> 1.6.8-0.1.testing.taw
  - 1.6.8 — https://github.com/laurent22/joplin/releases/tag/v1.6.8
  - Had to boost nodejs version requirements for SUSE Tumbleweed

* Sun Jan 03 2021 Todd Warner <t0dd_at_protonmail.com> 1.5.14-1.1.testing.taw
  - testing allowing builds on aarch64 --> FAILED (changes commented out)

* Sun Jan 03 2021 Todd Warner <t0dd_at_protonmail.com> 1.5.14-1.taw
* Sun Jan 03 2021 Todd Warner <t0dd_at_protonmail.com> 1.5.14-0.1.testing.taw
  - 1.5.14 — https://github.com/laurent22/joplin/releases/tag/v1.5.14

* Tue Dec 01 2020 Todd Warner <t0dd_at_protonmail.com> 1.4.19-1.taw
* Tue Dec 01 2020 Todd Warner <t0dd_at_protonmail.com> 1.4.19-0.1.testing.taw
  - 1.4.19 — https://github.com/laurent22/joplin/releases/tag/v1.4.19

* Tue Dec 01 2020 Todd Warner <t0dd_at_protonmail.com> 1.4.18-2.taw
* Tue Dec 01 2020 Todd Warner <t0dd_at_protonmail.com> 1.4.18-1.1.testing.taw
  - Fixing the RHEL8 builds by using nodejs from upstream.

* Sat Nov 28 2020 Todd Warner <t0dd_at_protonmail.com> 1.4.18-1.taw
* Sat Nov 28 2020 Todd Warner <t0dd_at_protonmail.com> 1.4.18-0.1.testing.taw
  - 1.4.18 — https://github.com/laurent22/joplin/releases/tag/v1.4.18

* Tue Nov 24 2020 Todd Warner <t0dd_at_protonmail.com> 1.4.12-1.1.testing.taw
* Tue Nov 24 2020 Todd Warner <t0dd_at_protonmail.com> 1.4.12-0.1.testing.taw
  - 1.4.12 pre-release — https://github.com/laurent22/joplin/releases/tag/v1.4.12
  - OpenSUSE 15.2 stopped building. Couldn't find /usr/bin/python -- fixed!

* Sat Nov 14 2020 Todd Warner <t0dd_at_protonmail.com> 1.4.10-0.1.testing.taw
  - 1.4.10 pre-release — https://github.com/laurent22/joplin/releases/tag/v1.4.10

* Fri Nov 13 2020 Todd Warner <t0dd_at_protonmail.com> 1.4.9-0.1.testing.taw
  - 1.4.9 pre-release — https://github.com/laurent22/joplin/releases/tag/v1.4.9
  - This version restructures the build with lerna and organizes the  
    application bits differently. So lots of changes from prior builds.  
    Yarn is no longer used for example. sqlite3 is pulled in by the build, etc.

* Sat Nov 7 2020 Todd Warner <t0dd_at_protonmail.com> 1.3.18-1.taw
* Sat Nov 7 2020 Todd Warner <t0dd_at_protonmail.com> 1.3.18-0.1.testing.taw
  - 1.3.18 release — https://github.com/laurent22/joplin/releases/tag/v1.3.18

* Thu Oct 29 2020 Todd Warner <t0dd_at_protonmail.com> 1.2.6-2.taw
* Thu Oct 29 2020 Todd Warner <t0dd_at_protonmail.com> 1.2.6-1.1.testing.taw
  - changes to get this to build on Fedora 33
  - python2 is no longer required to build the SQLite bits, thank god. Not  
    even shipped with Fedora 33. Updated the spec accordingly.
  - upstream tarball is no longer mirrored in the joplin-rpm github.  
    Redundant. Updated the spec accordingly.

* Fri Oct 9 2020 Todd Warner <t0dd_at_protonmail.com> 1.2.6-1.taw
* Fri Oct 9 2020 Todd Warner <t0dd_at_protonmail.com> 1.2.6-0.1.testing.taw
  - 1.2.6 release — https://github.com/laurent22/joplin/releases/tag/v1.2.6

* Wed Sep 30 2020 Todd Warner <t0dd_at_protonmail.com> 1.2.4-0.1.testing.taw
  - 1.2.4 pre-release — https://github.com/laurent22/joplin/releases/tag/v1.2.4

* Tue Sep 29 2020 Todd Warner <t0dd_at_protonmail.com> 1.2.3-0.1.testing.taw
  - 1.2.3 pre-release — https://github.com/laurent22/joplin/releases/tag/v1.2.3

* Mon Sep 21 2020 Todd Warner <t0dd_at_protonmail.com> 1.1.4-1.taw
* Mon Sep 21 2020 Todd Warner <t0dd_at_protonmail.com> 1.1.4-0.1.testing.taw
  - 1.1.4 release — https://github.com/laurent22/joplin/releases/tag/v1.1.4

* Thu Sep 17 2020 Todd Warner <t0dd_at_protonmail.com> 1.1.3-0.1.testing.taw
  - 1.1.3 pre-release — https://github.com/laurent22/joplin/releases/tag/v1.1.3

* Tue Sep 15 2020 Todd Warner <t0dd_at_protonmail.com> 1.1.2-0.1.testing.taw
  - 1.1.2 pre-release — https://github.com/laurent22/joplin/releases/tag/v1.1.2

* Wed Sep 09 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.245-1.taw
* Wed Sep 09 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.245-0.1.testing.taw
  - 1.0.245 release — https://github.com/laurent22/joplin/releases/tag/v1.0.245

* Sun Sep 06 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.242-1.taw
* Sun Sep 06 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.242-0.1.testing.taw
  - 1.0.242 release — https://github.com/laurent22/joplin/releases/tag/v1.0.242

* Wed Sep 02 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.239-0.1.testing.taw
  - 1.0.239 pre-release — https://github.com/laurent22/joplin/releases/tag/v1.0.239

* Sun Aug 02 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.233-1.taw
  - 1.0.233 release — https://github.com/laurent22/joplin/releases/tag/v1.0.233

* Sat Aug 01 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.233-0.1.testing.taw
  - 1.0.233 pre-release — https://github.com/laurent22/joplin/releases/tag/v1.0.233

* Wed Jul 29 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.232-0.1.testing.taw
  - 1.0.232 pre-release — https://github.com/laurent22/joplin/releases/tag/v1.0.232

* Sun Jul 26 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.231-0.3.testing.taw
  - builds for opensuse 15.1 are now successful as well

* Sun Jul 26 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.231-0.2.testing.taw
  - builds for opensuse 15.2 and tumbleweed are finally successful!

* Sat Jul 25 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.231-0.1.testing.taw
  - 1.0.231 pre-release - https://github.com/laurent22/joplin/releases/tag/v1.0.231
  - Also improved the .desktop file and made some other minor changes.

* Wed Jul 22 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.229-0.2.testing.taw
  - s/appdata.xml/metainfo.xml -- closer adherance to the freedesktop spec
  - installtree is now /usr/share/[appid]/
  - reducing the PNG icon set to 64, 128, 256, and 512

* Sat Jul 18 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.229-0.1.testing.taw
  - 1.0.229 pre-release — https://github.com/laurent22/joplin/releases/tag/v1.0.229
  - working towards OpenSUSE Leap 15.2 and Tumbleweed successful builds (not there yet)

* Sun Jul 12 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.227-1.taw
* Wed Jul 8 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.227-0.1.testing.taw
  - 1.0.227 — https://github.com/laurent22/joplin/releases/tag/v1.0.227

* Thu Jun 25 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.224-2.taw
* Thu Jun 25 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.224-1.1.testing.taw
  - icons need to be in desktop spec name ID format as well: org.joplinapp.Joplin.png/svg

* Tue Jun 23 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.224-1.taw
  - 1.0.224 — https://github.com/laurent22/joplin/releases/tag/v1.0.224

* Mon Jun 22 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.224-0.2.testing.taw
  - org.joplinapp.Joplin.desktop and org.joplinapp.Joplin.appdata.xml moved to  
    these names to be in compliance with:  
    https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html#file-naming  
    https://www.freedesktop.org/software/appstream/docs/chap-Metadata.html#sect-Metadata-GenericComponent
    https://dbus.freedesktop.org/doc/dbus-specification.html#message-protocol-names  
    https://docs.flatpak.org/en/latest/conventions.html  

* Sun Jun 21 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.224-0.1.testing.taw
  - 1.0.224 — https://github.com/laurent22/joplin/releases/tag/v1.0.224
  - Fixed regression
  - Improved: API: Improved error handling on service end-point
  - Fixed: API: Fixed externalEditWatcher/noteIsWatched call, fixed tests
  - New: API: Add support for external editing from API
  - New: Add default filename for jex export (#3034 by @CalebJohn)
  - New: Add swapLineUp and swapLineDown keys to Code Mirror editor (#3363 by @CalebJohn)
  - Improved: Do not expand the left notebook when following a link to a note
  - Improved: Reduce database logging statements
  - Improved: Remove auto-indent for in note html/xml for Code Mirror (#3374 by @CalebJohn)
  - Fixed: Fix getLineSpan logic and list token regex logic (#3365 by @CalebJohn)
  - Fixed: Fixed various bugs related to the import of ENEX files as HTML
  - Fixed: Prevent desktop.ini file from breaking sync lock (#3381)

* Sat Jun 13 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.220-0.1.testing.taw
  - 1.0.220 — <https://github.com/laurent22/joplin/releases/tag/v1.0.220>
  - Improved: Improved escaping of Markdown titles in links (#3333)
  - Improved: Refactored themes to allow using the same ones in both desktop  
    and mobile version
  - Fixed: Fixed issue with setting filename for edited attachments
  - Fixed: Prevent notebook to be the parent of itself (#3334)

* Sat Jun 13 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.218-1.taw
* Sun Jun 07 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.218-0.1.testing.taw
  - specfile: removed sed build requirement (a legacy requirement)
  - specfile: new BuildRequires: libsecret-devel
  - New editor: Code Mirror (potentially replacing Ace Editor?)
  - New translation (Bahasa Indonesian)
  - Improvement: Upload attachments > 4MB if you use OneDrive
  - And a whole pile of smaller improvements and fixes

* Mon Jun 01 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.216-3.taw
* Mon Jun 01 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.216-2.2.testing.taw
  - allowing OpenSuse 15.2 builds.

* Mon Jun 01 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.216-2.taw
* Mon Jun 01 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.216-1.2.testing.taw
* Tue May 26 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.216-1.1.testing.taw
  - First attempt at including the terminal application.
  - Added libnotify dependency. Technically optional but it makes things better.
  - Cleaned up provides and requires. autoreq pulls in far too much.

* Sun May 24 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.216-1.taw
* Sun May 24 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.216-0.1.testing.taw
  - 1.0.216
  - Fixed raw source links in specfile
  - First attempt at OpenSUSE build -- FAILED at npm install (failed husky install)

* Thu May 21 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.214-1..taw
* Thu May 21 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.214-0.1.testing.taw
  - 1.0.214

* Thu May 21 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.212-0.1.testing.taw
  - 1.0.212 testing

* Wed May 20 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.211-0.1.testing.taw
  - 1.0.211 testing

* Tue May 12 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.207-0.1.testing.taw
  - 1.0.207 testing

* Thu Apr 16 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.201-1.taw
* Thu Apr 16 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.201-0.1.testing.taw
  - 1.0.201

* Sun Apr 12 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.200-1.taw
* Sun Apr 12 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.200-0.1.testing.taw
  - 1.0.200

* Tue Mar 31 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.197-1.taw
* Tue Mar 31 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.197-0.1.testing.taw
  - 1.0.197

* Thu Mar 26 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.195-1.taw
* Thu Mar 26 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.195-0.1.testing.taw
  - 1.0.195

* Sat Mar 14 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.194-0.1.testing.taw
  - 1.0.194 -- hey, cool. Apparently this version comes with a WYSIWYG.
  - Seeing issues with not being able to switch documents via the sidebars.

* Sun Mar 08 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.193-1.1.testing.taw
  - added StartupWMClass window-grouping designation
  - updated XML metadata to include a history of versions

* Sun Mar 08 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.193-1.taw
* Sun Mar 08 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.193-0.2.testing.taw
  - 1.0.192 -- libcanberra-gtk2 dependency is not generated for some  
    reason. See https://discourse.joplinapp.org/t/dependency-on-canberra/6696

* Sun Mar 08 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.193-0.1.testing.taw
* Sat Mar 07 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.192-0.1.testing.taw
* Fri Mar 06 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.190-0.1.testing.taw
* Wed Mar 04 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.189-0.1.testing.taw
  - 1.0.189, 1.0.190, 1.0.192, 1.0.193

* Mon Mar 02 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.187-0.2.testing.taw
* Mon Mar 02 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.187-0.1.testing.taw
  - 1.0.187
  - The build process upstream was simplified which resulted in changes to the  
    spec

* Sat Jan 25 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.179-1.taw
* Sat Jan 25 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.179-0.1.testing.taw
  - 1.0.179

* Fri Jan 24 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.178-1.taw
* Fri Jan 24 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.178-0.3.testing.taw
  - 1.0.178 -- a "fatal error" is reported but it is an error in a git lookup  
    that otherwise does not break the build. The only work around (so far) is  
    what you see in 1.0.178-0.2 below which is not ideal. The error is  
    generated in the code found in ./ElectronClient/app/compile-package-info.js

* Fri Jan 24 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.178-0.2.testing.taw
  - 1.0.178 -- my own tarball generated from the git repo tag (and includes  
    git info) seems to work. Ugly, but it is a workaround.

* Tue Jan 21 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.178-0.1.testing.taw
  - 1.0.178 -- release tarball fails just like 1.0.177

* Fri Jan 17 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.177-0.2.testing.taw
* Wed Jan 01 2020 Todd Warner <t0dd_at_protonmail.com> 1.0.177-0.1.testing.taw
  - 1.0.177 -- fails to build correctly

* Mon Dec 16 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.176-0.1.testing.taw
  - 1.0.176
  - (specfile) fixed svg icon filename
  - (specfile) joplin should own individual icons, not the whole icon file tree

* Mon Dec 9 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.175-1.1.testing.taw
  - changed my mind on a naming scheme for an icon. Trivial, but it is indeed  
    a change.

* Mon Dec 9 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.175-1.taw
* Mon Dec 9 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.175-0.1.testing.taw
  - 1.0.175
  - icon was changed. I created highcontrast versions in contrib tarball and  
    they are deployed as they should be with the packaging into the desktop  
    environment.

* Sat Nov 16 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.174-1.1.testing.taw
  - specfile cleanup
  - contrib tarball cleanup

* Wed Nov 13 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.174-1.taw
* Wed Nov 13 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.174-0.1.testing.taw
  - 1.0.174
  - first successful build on Fedora 31 using an sqlite3 versioning hack  
    in package.json. Look what I did with sed and grep in the prep phase
  - and why the HECK does Joplin require python2 to build!?! Terrible.

* Mon Nov 11 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.173-1.taw
* Mon Nov 11 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.173-0.1.testing.taw
  - 1.0.173
  - problems with building on Fedora 31 due to python support issues

* Mon Oct 14 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.170-1.taw
* Mon Oct 14 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.170-0.1.testing.taw
  - 1.0.170
  - problems with building on Fedora 31 due to python support issues

* Sat Sep 28 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.169-0.1.testing.taw
  - 1.0.169
  - problems with building on Fedora 31 due to python support issues

* Wed Sep 25 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.168-1.taw
  - 1.0.168
  - problems with building on Fedora 31 due to python support issues

* Tue Sep 10 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.167-1.taw
  - 1.0.167 - fixes an upstream link management issue

* Mon Sep 09 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.166-1.taw
  - 1.0.166 - fixes an upstream PDF export issue

* Thu Aug 15 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.165-1.taw
  - 1.0.165

* Sun Jul 14 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.161-1.taw
  - 1.0.161

* Tue Jun 18 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.160-1.taw
* Tue Jun 18 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.160-0.1.testing.taw
  - 1.0.160

* Tue Jun 11 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.159-1.taw
* Tue Jun 11 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.159-0.1.testing.taw
  - 1.0.159

* Tue May 28 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.158-1.taw
* Tue May 28 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.158-0.1.testing.taw
  - 1.0.158

* Sun May 26 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.157-1.taw
* Fri May 24 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.157-0.1.testing.taw
  - 1.0.157

* Tue May 14 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.153-1.taw
* Tue May 14 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.153-0.1.testing.taw
  - 1.0.153

* Mon May 13 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.152-1.taw
* Mon May 13 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.152-0.1.testing.taw
  - 1.0.152

* Sun May 12 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.151-1.taw
* Sun May 12 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.151-0.1.testing.taw
  - 1.0.151

* Sat May 11 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.147-1.taw
* Sat May 11 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.147-0.1.testing.taw
  - 1.0.147

* Mon May 06 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.145-1.taw
* Mon May 06 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.145-0.1.testing.taw
  - 1.0.145
  - Note, have to tred carefully with npm update and audit fix.  
    Can lead to breakage and behavior is never certain.

* Wed May 01 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.144-1.taw
* Wed May 01 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.144-0.1.testing.taw
  - 1.0.144

* Mon Apr 22 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.143-1.taw
* Mon Apr 22 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.143-0.1.testing.taw
  - 1.0.143
  - normal soft break behavior rolled into the application. Woot.  
    https://github.com/laurent22/joplin/pull/1408

* Wed Apr 03 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.142-2.taw
* Wed Apr 03 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.142-1.1.testing.taw
  - a bit more checking during builds for existence of python symlink
  - have to force the path reset right prior to npm install for EL8 support

* Tue Apr 02 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.142-1.taw
* Tue Apr 02 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.142-0.1.testing.taw
  - 1.0.142

* Wed Mar 20 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.140-1.taw
* Tue Mar 19 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.140-0.1.testing.taw
  - 1.0.140
