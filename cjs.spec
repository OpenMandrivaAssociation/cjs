%global _internal_version  7a72175
%define api             1.0
%define major           0
%define girmajor        1.0
%define libname         %mklibname %{name} %{major}
%define develname       %mklibname -d %{name}
%define girname         %mklibname %{name}-gir %{girmajor}

# needed to prevent spurtious devel require
%global _requires_exclude devel\\(libmozjs\-24.*\\)

Name:          cjs
Epoch:         1
Version:       2.4.1
Release:       %mkrel 1
Summary:       Javascript Bindings for Cinnamon

Group:         Development/Other
# The following files contain code from Mozilla which
# is triple licensed under MPL1.1/LGPLv2+/GPLv2+:
# The console module (modules/console.c)
# Stack printer (gjs/stack.c)
License:       MIT and (MPLv1.1 or GPLv2+ or LGPLv2+)
URL:           http://cinnamon.linuxmint.com
# To generate tarball
# wget https://github.com/linuxmint/cjs/archive/%%{version}.tar.gz -O cjs-%%{version}.tar.gz
# for git
# wget https://github.com/linuxmint/cjs/tarball/%%{_internal_version} -O cjs-%%{version}.git%%{_internal_version}.tar.gz
#Source0:       http://leigh123linux.fedorapeople.org/pub/cjs/source/cjs-%{version}.git%{_internal_version}.tar.gz
Source0: http://leigh123linux.fedorapeople.org/pub/cjs/source/cjs-%{version}.tar.gz

BuildRequires: pkgconfig(mozjs-24)
BuildRequires: pkgconfig(cairo-gobject)
BuildRequires: pkgconfig(gobject-introspection-1.0) >= 1.31.22
BuildRequires: readline-devel
BuildRequires: pkgconfig(dbus-glib-1)
BuildRequires: intltool
# Bootstrap requirements
BuildRequires: gtk-doc
BuildRequires: gnome-common

%description
Cjs allows using Cinnamon libraries from Javascript. It's based on the
Spidermonkey Javascript engine from Mozilla and the GObject introspection
framework.

%package -n %{libname}
Group:          System/Libraries
Summary:        JavaScript bindings based on gobject-introspection

%description -n %{libname}
This package contains JavaScript bindings based on gobject-introspection.

%package -n %{develname}
Summary: Development package for %{name}
Group: Development/C
Requires:       %{libname} = %{?epoch}:%{version}-%{release}
Provides:       %{name}-devel = %{?epoch}:%{version}-%{release}
Provides:       lib%{name}-devel = %{?epoch}:%{version}-%{release}

%description -n %{develname}
Files for development with %{name}.

%package -n %{girname}
Summary:        GObject Introspection interface description for %{name}
Group:          System/Libraries
Requires:       %{libname} = %{?epoch}:%{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%prep
%setup -q 
sed -i -e 's@{ACLOCAL_FLAGS}@{ACLOCAL_FLAGS} -I m4@g' Makefile.am
echo "AC_CONFIG_MACRO_DIR([m4])" >> configure.ac
rm -f configure

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; fi;
 %configure2_5x --disable-static)
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make V=1

%install
%make_install

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%files
%doc COPYING COPYING.LGPL NEWS README
%{_bindir}/cjs
%{_bindir}/cjs-console

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{girname}
%{_libdir}/cjs/

%files -n %{develname}
%doc examples/*
%{_includedir}/cjs-1.0/
%{_libdir}/pkgconfig/cjs-*1.0.pc
%{_libdir}/*.so


%changelog
* Thu Nov 27 2014 joequant <joequant> 1:2.4.1-1.mga5
+ Revision: 799547
- 2.4.1

* Sun Nov 23 2014 joequant <joequant> 1:2.4.0-1.mga5
+ Revision: 798408
- upgrade to 2.4
- upgrade to 2.4
- upgrade to 2.2.2

  + umeabot <umeabot>
    - Second Mageia 5 Mass Rebuild
    - Rebuild to fix library dependencies
    - Mageia 5 Mass Rebuild

* Fri Apr 18 2014 joequant <joequant> 1:2.2.0-2.mga5
+ Revision: 616810
- upgrade to 2.2

* Mon Oct 21 2013 umeabot <umeabot> 1:2.0.0-2.mga4
+ Revision: 539577
- Mageia 4 Mass Rebuild

* Mon Oct 07 2013 joequant <joequant> 1:2.0.0-1.mga4
+ Revision: 492477
- update to 2.0.0

* Tue Oct 01 2013 joequant <joequant> 1:1.9.1-1.mga4
+ Revision: 490041
- update to 1.9.1

* Fri Aug 23 2013 joequant <joequant> 1.34.0-0.1.gitfb472ad.mga4
+ Revision: 470090
- imported package cjs

