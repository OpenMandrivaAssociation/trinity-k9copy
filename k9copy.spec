%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 3

%define tde_pkg k9copy
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		1.2.3
Release:		%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:		DVD backup tool for Trinity
Group:			Applications/Utilities
URL:			http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/multimedia/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:	  cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX="%{tde_prefix}"
BuildOption:    -DSHARE_INSTALL_PREFIX="%{tde_prefix}/share"
BuildOption:    -DINCLUDE_INSTALL_DIR="%{tde_prefix}/include"
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}

BuildRequires:	desktop-file-utils
BuildRequires:	trinity-k3b-devel

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig

# Warning: the target distribution must have ffmpeg !
BuildRequires:	pkgconfig(libavcodec)

# DVDREAD support
BuildRequires:  pkgconfig(dvdread)

# MESA support
BuildRequires:  pkgconfig(glu)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
k9copy is a tabbed tool that allows to copy of one or more titles from a DVD9
to a DVD5, in thesame way than DVDShrink for Microsoft Windows (R).
This is the Trinity version.

%prep -a
# Removes internal dvdread headers
%__rm -rf "dvdread"

# Fix permissions on doc files
chmod -x AUTHORS COPYING


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"

# FFMPEG ...
if [ -d /usr/include/ffmpeg ]; then
  %{optflags}="%{optflags} -I/usr/include/ffmpeg"
fi


%install -a
%find_lang %{tde_pkg}


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_prefix}/bin/k9copy
%{tde_prefix}/share/applications/tde/k9copy.desktop
%{tde_prefix}/share/apps/k9copy/
%{tde_prefix}/share/apps/konqueror/servicemenus/k9copy_open.desktop
%lang(en) %{tde_prefix}/share/doc/tde/HTML/en/k9copy/
%{tde_prefix}/share/icons/hicolor/*/apps/k9copy.png
%{tde_prefix}/share/man/man1/k9copy.1*

