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
%define name_cli joplin-cli
%define name_desktop joplin-desktop
Summary: A free and secure notebook application

%define targetIsProduction 0
%define nativebuild 1

# Only used if the dev team or the RPM builder includes things like rc3 or the
# date in the source filename
%define buildQualifier 20190226
%undefine buildQualifier

# VERSION
%define vermajor 1.0
%define verminor 187
Version: %{vermajor}.%{verminor}

# RELEASE
%define _pkgrel 1
%if ! %{targetIsProduction}
  %define _pkgrel 0.2
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
BuildRequires: python sed grep
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

echo "======== prep stage ========"

rm -rf %{sourceroot} ; mkdir -p %{sourceroot}

# The prep section is the first place we can run shell commands. Therefore,
# these checks are here...
%if 0%{?suse_version:1}
  echo "======== Opensuse version: %{suse_version}"
  echo "Builds for OpenSUSE are not currently supported."
  exit 1
%endif
%if 0%{?fedora:1}
  echo "======== Fedora version: %{fedora}"
%if 0%{?fedora} <= 28
  echo "Builds for Fedora 28 and older are no longer supported."
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


%if 0%{?fedora:1}
  echo "======== Forcing python2 availability for SQLite build requirements"
  mkdir -p $HOME/.local/bin
  if [ ! -e "$HOME/.local/bin/python" ] ;  then
    ln -s /usr/bin/python2 $HOME/.local/bin/python
  fi
#%%if 0%%{?fedora} > 30
#  # THIS IS NOT WORKING
#  mkdir -p %%{sourcetree}/ElectronClient/app/node_modules
#  mkdir -p %%{sourcetree}/CliClient/node_modules
#  cp -aL --no-preserve=ownership /usr/lib/node_modules/sqlite3 %%{sourcetree}/ElectronClient/app/node_modules/sqlite3
#  cp -aL --no-preserve=ownership /usr/lib/node_modules/sqlite3 %%{sourcetree}/CliClient/node_modules/sqlite3

#  # THIS _IS_ WORKING (joplin 1.0.174 to 1.0.179)
#  # This is a hack, but the various package.json files have too old of a sqlite3 version declared
#  grep '"version"' /usr/lib/node_modules/sqlite3/package.json > temp.json
#  nodejs_sqlite3_version=$(sed -nre 's/^[^0-9]*(([0-9]+\.)*[0-9]+).*/\1/p' temp.json)
#  sed -i.bak '/sqlite/c\    "sqlite3": "^'${nodejs_sqlite3_version}'",' %{sourcetree}/ElectronClient/app/package.json
#  sed -i.bak '/sqlite/c\    "sqlite3": "^'${nodejs_sqlite3_version}'",' %{sourcetree}/CliClient/package.json
#  rm temp.json

#%%endif
#%%if 0%%{?fedora} > 30
#  # NOTE: THIS IS EXPERIMENTAL AND LIKELY TO BE REMOVED
#  cd %%{sourcetree}
#  # desktop -- strip out certain packages from json file
#  cd ElectronClient/app
#  grep -v sqlite3 package.json > temp.json
#  mv temp.json package.json
#  rm package-lock.json
#  cd ../..
#  cd CliClient
#  grep -v sqlite3 package.json > temp.json
#  mv temp.json package.json
#  rm package-lock.json
#  cd ..
#  cd Tools
#  grep -v sqlite3 package.json > temp.json
#  mv temp.json package.json
#  rm package-lock.json
#  cd ..
#  cd ..
#%%endif
%endif

%if 0%{?rhel:1}
%if 0%{?rhel} >= 8
  # This is ugly. But EL8 doesn't have /usr/bin/python
  # /usr/bin/python is going away: https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/
  # ...brute forcing things...
  echo "======== Forcing python2 availability for SQLite build requirements"
  mkdir -p $HOME/.local/bin
  if [ ! -e "$HOME/.local/bin/python" ] ;  then
    ln -s /usr/bin/python2 $HOME/.local/bin/python
  fi
%endif
%endif



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

### BUILD IT!
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
Exec=%{name_desktop}
Icon=%{name}
Terminal=false
Categories=Office;
Keywords=secure;security;privacy;private;notes;bookmarks;collaborate;research;
StartupNotify=true
X-Desktop-File-Install-Version=0.23
" > %{buildroot}%{_datadir}/applications/%{name}.desktop
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/256x256.png   %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/32x32.png     %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/16x16.png     %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/128x128.png   %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/96x96.png     %{buildroot}%{_datadir}/icons/hicolor/96x96/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/1024x1024.png %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/24x24.png     %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/144x144.png   %{buildroot}%{_datadir}/icons/hicolor/144x144/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/72x72.png     %{buildroot}%{_datadir}/icons/hicolor/72x72/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/LinuxIcons/512x512.png   %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
install -D -m644 -p %{sourcetree}/Assets/JoplinIcon.svg           %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

install -D -m644 -p %{sourcetree_contrib}/desktop-icons/256x256-highcontrast.png    %{buildroot}%{_datadir}/icons/HighContrast/256x256/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/32x32-highcontrast.png      %{buildroot}%{_datadir}/icons/HighContrast/32x32/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/16x16-highcontrast.png      %{buildroot}%{_datadir}/icons/HighContrast/16x16/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/128x128-highcontrast.png    %{buildroot}%{_datadir}/icons/HighContrast/128x128/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/96x96-highcontrast.png      %{buildroot}%{_datadir}/icons/HighContrast/96x96/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/1024x1024-highcontrast.png  %{buildroot}%{_datadir}/icons/HighContrast/1024x1024/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/24x24-highcontrast.png      %{buildroot}%{_datadir}/icons/HighContrast/24x24/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/144x144-highcontrast.png    %{buildroot}%{_datadir}/icons/HighContrast/144x144/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/72x72-highcontrast.png      %{buildroot}%{_datadir}/icons/HighContrast/72x72/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/512x512-highcontrast.png    %{buildroot}%{_datadir}/icons/HighContrast/512x512/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop-icons/JoplinIcon-highcontrast.svg %{buildroot}%{_datadir}/icons/HighContrast/scalable/apps/%{name}.svg

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
rm -rf $(find %{sourcetree}/ElectronClient/dist/linux-unpacked/resources/app*/node_modules/7zip-bin-linux/* -type d | grep -v x64)
%else
rm -rf $(find %{sourcetree}/ElectronClient/dist/linux-unpacked/resources/app*/node_modules/7zip-bin-linux/* -type d | grep -v ia32)
%endif
cp -a %{sourcetree}/CliClient/build/* %{buildroot}%{installtree}/cli/
cp -a %{sourcetree}/ElectronClient/dist/linux-unpacked/* %{buildroot}%{installtree}/desktop/
# a little ugly
ln -s %{installtree}/cli/main.js %{buildroot}%{installtree}/cli/%{name_cli}
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
# desktop environment metadata
%{_datadir}/applications/%{name}.desktop
%{_metainfodir}/%{name}.appdata.xml
# desktop environment icons
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/96x96/apps/%{name}.png
%{_datadir}/icons/hicolor/1024x1024/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/144x144/apps/%{name}.png
%{_datadir}/icons/hicolor/72x72/apps/%{name}.png
%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/icons/HighContrast/256x256/apps/%{name}.png
%{_datadir}/icons/HighContrast/32x32/apps/%{name}.png
%{_datadir}/icons/HighContrast/16x16/apps/%{name}.png
%{_datadir}/icons/HighContrast/128x128/apps/%{name}.png
%{_datadir}/icons/HighContrast/96x96/apps/%{name}.png
%{_datadir}/icons/HighContrast/1024x1024/apps/%{name}.png
%{_datadir}/icons/HighContrast/24x24/apps/%{name}.png
%{_datadir}/icons/HighContrast/144x144/apps/%{name}.png
%{_datadir}/icons/HighContrast/72x72/apps/%{name}.png
%{_datadir}/icons/HighContrast/512x512/apps/%{name}.png
%{_datadir}/icons/HighContrast/scalable/apps/%{name}.svg

%if 0%{?nativebuild:1}
# /usr/share/joplin
%{installtree}
#%%{_bindir}/%%{name_cli}
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
