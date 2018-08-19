%define url_ver	%(echo %{version}|cut -d. -f1,2)
%define _disable_rebuild_configure 1

%define api	3
%define major	15
%define gimajor	3.0
%define libname	%mklibname gweather %{api} %{major}
%define girname	%mklibname gweather-gir %{gimajor}
%define devname	%mklibname -d gweather

Summary:	GNOME Weather applet library
Name:		libgweather
Version:	3.28.2
Release:	1
License:	GPLv2+
Group:		System/Libraries
Url:		http://www.gnome.org
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/libgweather/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	libxml2-utils
BuildRequires:	pkgconfig(gconf-2.0) GConf2
BuildRequires:	pkgconfig(geocode-glib-1.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libsoup-gnome-2.4)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	timezone
BuildRequires:  meson
BuildRequires:  pkgconfig(vapigen)

%description
This is a library to provide Weather data to the GNOME panel applet.

%package -n %{libname}
Group:		System/Libraries
Summary:	GNOME Weather applet library
Requires:	%{name} >= %{version}-%{release}

%description -n %{libname}
This is a library to provide Weather data to the GNOME panel applet.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{devname}
Group:		Development/C
Summary:	GNOME Weather applet library
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the development files for %{name}.

%prep
%setup -q

%build
%meson -Denable_vala=true -Dgtk_doc=true

%meson_build

%install
%meson_install
%find_lang %{name}-3.0
%find_lang %{name}-locations
cat %{name}-locations.lang >> %{name}-3.0.lang

%files -f %{name}-3.0.lang

%doc AUTHORS NEWS
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/locations.dtd
%{_datadir}/%{name}/Locations.xml
%{_datadir}/glib-2.0/schemas/org.gnome.GWeather.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.GWeather.gschema.xml

%files -n %{libname}
%{_libdir}/libgweather-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/GWeather-%{gimajor}.typelib

%files -n %{devname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/gtk-doc/html/%{name}-3.0
%{_datadir}/gir-1.0/GWeather-%{gimajor}.gir

