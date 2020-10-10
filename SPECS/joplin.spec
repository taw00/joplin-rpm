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
%define vermajor 1.2
%define verminor 6
Version: %{vermajor}.%{verminor}

# RELEASE
%define _pkgrel 1
%if ! %{targetIsProduction}
  %define _pkgrel 0.1
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
# Note, for example, this will not build on ppc64le
ExclusiveArch: x86_64 i686 i586 i386

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

Source0: https://github.com/taw00/joplin-rpm/raw/master/SOURCES/%{sourcetree}.tar.gz
Source1: https://github.com/taw00/joplin-rpm/raw/master/SOURCES/%{sourcetree_contrib}.tar.gz

# See https://discourse.joplinapp.org/t/dependency-on-canberra/6696
Requires: libcanberra-gtk2 libnotify
Requires: libnotify

# Including the terminal client tree really does a number on dependencies. We
# need to filter things.
# Desktop will include some silly scans for provides and deps as well
%global __provides_exclude_from ^(.%{installtree}/.*\\.so.*|%{installtree}/cli/node_modules/.*|%{installtree}/cli/build/.*|%{installtree}/cli/tests/.*|%{installtree}/desktop/resources/.*)$
%global __requires_exclude_from ^(.%{installtree}/.*\\.so.*|%{installtree}/cli/node_modules/.*|%{installtree}/cli/build/.*|%{installtree}/cli/tests/.*|%{installtree}/desktop/resources/.*)$
%global __provides_exclude ^(lib.*\\.so.*)$
%global __requires_exclude ^((libffmpeg[.]so.*)|(lib.*\\.so.*)|(/usr/bin.*/coffee))$

# provided by coreutils RPM
#BuildRequires: /usr/bin/readlink /usr/bin/dirname

BuildRequires: libsecret-devel

BuildRequires: git rsync findutils grep
BuildRequires: desktop-file-utils

%if 0%{?suse_version:1}
BuildRequires: ca-certificates-cacert ca-certificates-mozilla ca-certificates
BuildRequires: appstream-glib
# For Leap 15.2, to be able to include yarn, we had to add this repo to the build system
# https://download.opensuse.org/repositories/devel:/languages:/nodejs/openSUSE_Leap_15.2/
BuildRequires: nodejs12 npm12 nodejs12-devel nodejs-common yarn
BuildRequires: python2 gcc-c++
%if 0%{?sle_version}
# Leap
%if 0%{?sle_version} == 150100
# Leap 15.1
%endif
%if 0%{?sle_version} == 150200
# Leap 15.2
%endif
%else
# Tumbleweed
%endif
%endif

%if 0%{?rhel:1}
BuildRequires: libappstream-glib
%if 0%{?rhel} < 8
# EL7 -- This is super ugly
# EL7 is too far behind on many many packages (EL7 is based on F19 and F20).
# Therefore, you have to pull from some RPMs from other repos. In this case,
# nodejs and yarn. Include these repos into your mock or build environments...
#   https://rpm.nodesource.com/pub_10.x/el/7/$basearch
#   https://dl.yarnpkg.com/rpm/
# Note that this version of nodejs installs npm as well.
BuildRequires: nodejs >= 2:10
BuildRequires: yarn
BuildRequires: python
%else
# EL8 is based on Fedora 28 (sorta)
# Note: /usr/bin/python is going away -- https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/
BuildRequires: nodejs npm python2
%endif
%endif

%if 0%{?fedora:1}
BuildRequires: libappstream-glib
# Note: /usr/bin/python is going away -- https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/
BuildRequires: python
BuildRequires: nodejs-sqlite3
#%%if 0%%{?fedora} <= 30
BuildRequires: nodejs npm nodejs-yarn node-gyp
#%%endif
%if 0%{?fedora} >= 31
BuildRequires: python2
%endif
%endif



#t0dd: I often add these extra packages to enable mock environment introspection
%if ! %{targetIsProduction}
#BuildRequires: tree vim-enhanced less findutils
BuildRequires: tree vim-enhanced less
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
%if 0%{?fedora:1}
  echo "======== Fedora version: %{fedora}"
  %if 0%{?fedora} <= 29
    echo "Builds for Fedora 29 and older are no longer supported."
    exit 1
  %endif
%endif
%if 0%{?rhel:1}
  echo "======== EL version: %{rhel}"
  %if 0%{?rhel} < 7
    echo "Builds for EL 6 and older are not supported."
    exit 1
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

echo "======== Forcing python2 availability for SQLite build requirements"
mkdir -p $HOME/.local/bin
if [ ! -e "$HOME/.local/bin/python" ] ;  then
  ln -s /usr/bin/python2 $HOME/.local/bin/python
fi

# For debugging purposes...
%if ! %{targetIsProduction}
  cd .. ; tree -d -L 2 %{sourceroot} ; cd -
%endif


%build
# Build section starts us in directory {_builddir}/{sourceroot}
echo "======== build stage ========"

cd %{sourcetree}

%if 0%{?fedora:1}
# Fedora 29+ (executable is yarnpkg and not yarn)
%if 0%{?fedora} >= 29
  #if [ "$?" -ne 0 ] ; then
  echo "======== Mapping yarnpkg to 'yarn' as build scripts expect"
  mkdir -p $HOME/.local/bin
  if [ ! -e "$HOME/.local/bin/yarn" ] ;  then
    ln -s /usr/bin/yarnpkg $HOME/.local/bin/yarn
  fi

# Fedora 28-
%else
  # NOTE: This is here for posterity. We are no longer building for Fedora 28
  #       and older.
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

# EL7 and 8
%if 0%{?rhel:1}
%if 0%{?rhel} >= 8
  npm install gyp
  npm install yarn
  _pwd=$(pwd)
  echo "======== Mapping yarn so it can be found in the path"
  mkdir -p $HOME/.local/bin
  if [ ! -e "$HOME/.local/bin/yarn" ] ;  then
    ln -s ${_pwd}/node_modules/.bin/yarn $HOME/.local/bin/yarn
  fi
%endif
  yarn add electron-builder --dev
  yarn add electron-packager --dev
%endif

echo "###### NOTE: You will see the build gripe about a husky build failure because a .git can't be found. Ignore this #######"

### BUILD IT!
# This npm install will trigger these set of events:
# cd Tools && npm i && cd .. && cd ReactNativeClient && npm i && cd .. && cd ElectronClient && npm i && cd .. && cd CliClient && npm i && cd .. && gulp build
npm install
cd ElectronClient
yarn dist
cd ..


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
install -d %{buildroot}%{installtree}/cli
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
# Strip out irrelevant 7zip-bin architecture builds. This is ugly, but (a)
# those bits are superfluous, and (b) they add dependencies that can't be met.
# Question I have is... do we need 7zip-bin? Probably, so leaving it in.
#%%if "%%{?_lib}" == "lib64"
%ifarch x86_64 amd64
rm -rf $(find %{sourcetree}/ElectronClient/dist/linux-unpacked/resources/app*/node_modules/7zip-bin-linux/* -type d | grep -v x64)
%else
rm -rf $(find %{sourcetree}/ElectronClient/dist/linux-unpacked/resources/app*/node_modules/7zip-bin-linux/* -type d | grep -v ia32)
%endif
cp -a %{sourcetree}/CliClient/* %{buildroot}%{installtree}/cli
cp -a %{sourcetree}/ElectronClient/dist/linux-unpacked/* %{buildroot}%{installtree}/desktop/
# a little ugly
ln -s %{installtree}/cli/build/main.js %{buildroot}%{installtree}/cli/%{name}
ln -s %{installtree}/cli/%{name} %{buildroot}%{_bindir}/%{name_cli}
ln -s %{installtree}/desktop/joplin %{buildroot}%{installtree}/desktop/%{name_desktop}
ln -s %{installtree}/desktop/joplin %{buildroot}%{_bindir}/%{name_desktop}

# AppImage build
%else
# This is SUPER ugly... It's an alternative if we want to use it.
install -D -m755 -p %{sourcetree}/ElectronClient/dist/'Joplin '%{version}'.AppImage' %{buildroot}%{_bindir}/%{name_desktop}
%endif


%files
%defattr(-,root,root,-)
%license %{sourcetree}/LICENSE
%doc %{sourcetree}/ElectronClient/dist/linux-unpacked/LICENSE.electron.txt
%doc %{sourcetree}/ElectronClient/dist/linux-unpacked/LICENSES.chromium.html
%{_bindir}/%{name_desktop}
%{_bindir}/%{name_cli}
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

* Wed Sep 15 2020 Todd Warner <t0dd_at_protonmail.com> 1.1.2-0.1.testing.taw
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
