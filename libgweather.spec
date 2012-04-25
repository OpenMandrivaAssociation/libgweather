%define url_ver	%(echo %{version}|cut -d. -f1,2)


%define api		3
%define major		0
%define gir_major	3.0

%define libname		%mklibname gweather %{api} %{major}
%define develname	%mklibname -d gweather
%define girname		%mklibname gweather-gir %{gir_major}
%define olddevelname %mklibname -d gnome-applets

Summary: GNOME Weather applet library
Name: libgweather
Version: 3.4.1
Release: 2
License: GPLv2+
Group: System/Libraries
Url: http://www.gnome.org
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/libgweather/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	libxml2-utils
BuildRequires:	pkgconfig(gconf-2.0) GConf2
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libsoup-gnome-2.4)
BuildRequires:	pkgconfig(libxml-2.0)

%description
This is a library to provide Weather data to the GNOME panel applet.

%package -n %{libname}
Group: System/Libraries
Summary: GNOME Weather applet library
Requires: %{name} >= %{version}-%{release}

%description -n %{libname}
This is a library to provide Weather data to the GNOME panel applet.

%package -n %{girname}
Summary: GObject Introspection interface description for %{name}
Group: System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{develname}
Group: Development/C
Summary: GNOME Weather applet library
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Obsoletes: %olddevelname < 2.21.3

%description -n %{develname}
This is a library to provide Weather data to the GNOME panel applet.

%prep
%setup -q

%build
%configure2_5x \
	--enable-introspection=yes \
	--disable-static \
	--disable-gtk-doc 

%make 

%install
%makeinstall_std
%find_lang %{name}-3.0
find %{buildroot} -name '*.la' -exec rm -f {} ';'

for xmlfile in  %{buildroot}%{_datadir}/%{name}/Locations.*.xml; do
echo "%lang($(basename $xmlfile|sed -e s/Locations.// -e s/.xml//)) $(echo $xmlfile | sed s!%{buildroot}!!)" >> %{name}-3.0.lang
done

%preun
%preun_uninstall_gconf_schemas gweather

%files -f %{name}-3.0.lang
%doc AUTHORS NEWS
%{_sysconfdir}/gconf/schemas/gweather.schemas
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/locations.dtd
%{_datadir}/%{name}/Locations.xml
%{_datadir}/icons/gnome/*/status/weather*

%files -n %{libname}
%{_libdir}/libgweather-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/GWeather-%{gir_major}.typelib

%files -n %{develname}
%doc ChangeLog
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/gtk-doc/html/%{name}-3.0
%{_datadir}/gir-1.0/GWeather-%{gir_major}.gir

