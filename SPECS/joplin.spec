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
%define name2 joplin-desktop
Summary: A free and secure notebook application

%define targetIsProduction 1
%define nativebuild 1

# Only used if the dev team or the RPM builder includes things like rc3 or the
# date in the source filename
%define buildQualifier 20190226
%undefine buildQualifier

# VERSION
%define vermajor 1.0
%define verminor 142
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

%define snapinfo testing
%if %{targetIsProduction}
  %undefine snapinfo
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
URL: https://joplin.cozic.net/
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
%define installtree %{_datadir}/%{name}

Source0: https://github.com/taw00/joplin-rpm/blob/master/SOURCES/%{sourcetree}.tar.gz
Source1: https://github.com/taw00/joplin-rpm/blob/master/SOURCES/%{sourcetree_contrib}.tar.gz

# provided by coreutils RPM
#BuildRequires: /usr/bin/readlink /usr/bin/dirname

%if 0%{?rhel:1}
BuildRequires: git rsync findutils 
BuildRequires: desktop-file-utils
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
BuildRequires: git rsync findutils 
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
# Note: /usr/bin/python is going away -- https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/
BuildRequires: python
%if 0%{?fedora} >= 29
BuildRequires: nodejs npm nodejs-yarn node-gyp
%else
BuildRequires: nodejs npm node-gyp
%endif
%endif



#t0dd: I often add these extra packages to enable mock environment introspection
%if ! %{targetIsProduction}
#BuildRequires: tree vim-enhanced less findutils
BuildRequires: tree vim-enhanced less
%endif


%description
Joplin is a free and secure notebook application. Organization is easy using
notebooks and tags which can all be synchronized between your various devices.
The notes are can be searched, copied, tagged, and modified either from the
applications directly or from your own favorite text editor. The notes are
composed with the ever-popular and familiar markdown format.

Notes can be imported from Evernote, to include all associated resources
(images, attachments, etc) and all metadata (geo-location, update time,
creation time, etc). Notes can, of course, also be imported from any other
markdown source.

Mirroring to your devices and redundancy is achieved by a simple, and
optionally encrypted, synchronization to various cloud services including
Nextcloud, Dropbox, Onedrive, WebDAV, or your local or network-accessible file
system.


%prep
# Prep section starts us in directory {_builddir}
rm -rf %{sourceroot} ; mkdir -p %{sourceroot}

# The prep section is the first place we can run shell commands. Therefore,
# these checks are here...
%if 0%{?suse_version:1}
echo "======== Opensuse version: %{suse_version}"
echo "Right now... OpenSUSE is not supported. Sorry."
exit 1
echo "Supporting ANY version of opensuse is a struggle. Fair warning."
%endif

%if 0%{?fedora:1}
echo "======== Fedora version: %{fedora}"
#%%if 0%%{?fedora} == 28
#  echo "Fedora 28 can't be supported. Sorry."
#  exit 1
#%%endif
%if 0%{?fedora} < 28
  echo "Fedora 27 and older can't be supported. Sorry."
  exit 1
%endif
%endif

%if 0%{?rhel:1}
echo "======== EL version: %{rhel}"
%if 0%{?rhel} < 7
  echo "EL 6 and older can't be supported. Sorry."
  exit 1
%endif
%if 0%{?rhel} >= 8
  # This is ugly. But EL8 doesn't have /usr/bin/python
  # /usr/bin/python is going away -- https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/
  mkdir -p $HOME/.local/bin
  ln -s /usr/bin/python2 $HOME/.local/bin/python
%endif
%endif

# Unarchived source tree structure (extracted in {_builddir})
#   sourceroot             joplin-1.0
#    \_{sourcetree}          \_joplin-1.0.140
#    \_{sourcetree_contrib}  \_joplin-1.0-contrib

# Extract into {_builddir}/{sourceroot}/
# Source0:...
%setup -q -T -D -a 0 -n %{sourceroot}
# Source1:...
%setup -q -T -D -a 1 -n %{sourceroot}

# For debugging purposes...
%if ! %{targetIsProduction}
  cd .. ; tree -d -L 2 %{sourceroot} ; cd -
%endif


%build
# Build section starts us in directory {_builddir}/{sourceroot}
cd %{sourcetree}

#
# tools (supportive)
#
cd Tools
npm install
npm audit fix
cd ..

#
# desktop app
#
cd ElectronClient/app
rsync --delete -a ../../ReactNativeClient/lib/ lib/
npm install
npm audit fix

%if 0%{?fedora:1}
# Fedora 29+
%if 0%{?fedora} >= 29
  echo "\
# nodejs-yarn installs /usr/bin/yarnpkg for some reason (conflicts?). So, we
# simply alias it so that embedded scripts don't stumble over this anomaly
alias yarn='/usr/bin/yarnpkg'" >> ~/.bashrc
  source ~/.bashrc
# Fedora 28-
%else
  npm install yarn
  _pwd=$(pwd)
  echo "\
alias yarn='${_pwd}/node_modules/.bin/yarn'" >> ~/.bashrc
  source ~/.bashrc
  yarn add electron-builder --dev
  yarn add electron-packager --dev
%endif
%endif

# EL7 and 8
%if 0%{?rhel:1}
%if 0%{?rhel} >= 8
  npm install yarn
  npm install gyp
  _pwd=$(pwd)
  echo "\
alias yarn='${_pwd}/node_modules/.bin/yarn'" >> ~/.bashrc
  source ~/.bashrc
%endif
  yarn add electron-builder --dev
  yarn add electron-packager --dev
%endif

# all versions of OS
yarn dist
cd ../..

#
# commandline app
#
cd CliClient
npm install
npm audit fix
./build.sh
rsync --delete -aP ../ReactNativeClient/locales/ build/locales/
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
#  Note: We install to /usr/share/ because /opt is for unpackaged applications
#        http://www.pathname.com/fhs/pub/fhs-2.3.html

# Create directories
install -d %{buildroot}%{_libdir}/%{name}
install -d -m755 -p %{buildroot}%{_bindir}
install -d %{buildroot}%{installtree}/desktop
install -d %{buildroot}%{installtree}/cli
install -d %{buildroot}%{_datadir}/applications
%define _metainfodir %{_datadir}/metainfo
install -d %{buildroot}%{_metainfodir}

echo "[Desktop Entry]
Type=Application
Name=Joplin
GenericName=Secure notes
Comment=A secure notebook
Exec=%{name2}
Icon=%{name}
Terminal=false
Categories=Office;
Keywords=secure;security;privacy;private;notes;bookmarks;collaborate;research;
StartupNotify=true
X-Desktop-File-Install-Version=0.23
" > %{buildroot}%{_datadir}/applications/%{name}.desktop
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/256x256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/32x32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/16x16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/96x96.png %{buildroot}%{_datadir}/icons/hicolor/96x96/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/1024x1024.png %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/24x24.png %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/144x144.png %{buildroot}%{_datadir}/icons/hicolor/144x144/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/72x72.png %{buildroot}%{_datadir}/icons/hicolor/72x72/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/512x512.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
install -D -m644 -p %{sourcetree_contrib}/%{name}.appdata.xml %{buildroot}%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

# Native build
%if 0%{?nativebuild:1}
# Strip out irrelevant 7zip-bin architecture builds. This is ugly, but (a)
# those bits are superfluous, and (b) they add dependencies that can't be met.
# Question I have is... do we need 7zip-bin? Probably, so leaving it in.
#%%if "%%{?_lib}" == "lib64"
%ifarch x86_64 amd64
rm -rf $(find %{sourcetree}/ElectronClient/app/dist/linux-unpacked/resources/app/node_modules/7zip-bin-linux/* -type d | grep -v x64)
%else
rm -rf $(find %{sourcetree}/ElectronClient/app/dist/linux-unpacked/resources/app/node_modules/7zip-bin-linux/* -type d | grep -v ia32)
%endif
cp -a %{sourcetree}/CliClient/build/* %{buildroot}%{installtree}/cli/
cp -a %{sourcetree}/ElectronClient/app/dist/linux-unpacked/* %{buildroot}%{installtree}/desktop/
# a little ugly
ln -s %{installtree}/cli/main.js %{buildroot}%{_bindir}/%{name}
ln -s %{installtree}/desktop/joplin %{buildroot}%{_bindir}/%{name2}

# AppImage build
%else
# This is SUPER ugly... It's an alternative if we want to use it.
install -D -m755 -p %{sourcetree}/ElectronClient/app/dist/'Joplin 1.0.140.AppImage' %{buildroot}%{_bindir}/%{name2}
%endif


%files
%defattr(-,root,root,-)
%license %{sourcetree}/LICENSE
%doc %{sourcetree}/ElectronClient/app/dist/linux-unpacked/LICENSE.electron.txt
%doc %{sourcetree}/ElectronClient/app/dist/linux-unpacked/LICENSES.chromium.html
%{_bindir}/%{name2}
%{_datadir}/icons/*
%{_datadir}/applications/%{name}.desktop
%{_metainfodir}/%{name}.appdata.xml

%if 0%{?nativebuild:1}
# /usr/share/joplin
%{installtree}
%{_bindir}/%{name}
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
* Tue Apr 02 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.142-1.taw
* Tue Apr 02 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.142-0.1.testing.taw
  - 1.0.142

* Wed Mar 20 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.140-1.taw
* Tue Mar 19 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.140-0.1.testing.taw
  - 1.0.140
