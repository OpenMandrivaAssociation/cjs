%define api             1.0
%define major           0
%define girmajor        1.0
%define libname         %mklibname %{name} %{major}
%define develname       %mklibname -d %{name}
%define girname         %mklibname %{name}-gir %{girmajor}

# needed to prevent spurtious devel require
%define __noautoreq 'devel\\(libmozjs-78.*'

Name:          cjs
Epoch:         1
Version:       5.8.0
Release:       1
Summary:       Javascript Bindings for Cinnamon

Group:         Development/Other
# The following files contain code from Mozilla which
# is triple licensed under MPL1.1/LGPLv2+/GPLv2+:
# The console module (modules/console.c)
# Stack printer (gjs/stack.c)
License:       MIT and (MPLv1.1 or GPLv2+ or LGPLv2+)
URL:           http://cinnamon.linuxmint.com

Source0: https://github.com/linuxmint/cjs/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: meson
BuildRequires: dbus-daemon
BuildRequires: pkgconfig(mozjs-102)
BuildRequires: pkgconfig(cairo-gobject)
BuildRequires: pkgconfig(gobject-introspection-1.0) >= 1.31.22
BuildRequires: pkgconfig(sysprof-capture-4)
BuildRequires: readline-devel
BuildRequires: pkgconfig(dbus-glib-1)
BuildRequires: intltool
# Bootstrap requirements
BuildRequires: gtk-doc
BuildRequires: gnome-common
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk+-3.0)

Requires: gobject-introspection
Requires: gtk+3
Requires: mozjs78
Requires: glib2

%description
Cjs allows using Cinnamon libraries from Javascript. It's based on the
Spidermonkey Javascript engine from Mozilla and the GObject introspection
framework.

%package -n %{libname}
Group:          System/Libraries
Summary:        JavaScript bindings based on gobject-introspection
#Requires:	typelib(CjsPrivate)

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
%autopatch -p1

%build
%meson -Dinstalled_tests=false
%meson_build

%install
%meson_install

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%files
%doc COPYING NEWS README.md
%{_bindir}/cjs
%{_bindir}/cjs-console
%{_datadir}/%{name}-%{api}/lsan/lsan.supp
%{_datadir}/%{name}-%{api}/valgrind/gjs.supp

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{girname}
%{_libdir}/cjs/

%files -n %{develname}
%doc examples/*
%{_includedir}/cjs-1.0/
%{_libdir}/pkgconfig/cjs-*1.0.pc
%{_libdir}/*.so
