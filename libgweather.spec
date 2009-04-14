%define name libgweather
%define version 2.26.1
%define release %mkrel 1
%define major 1
%define libname %mklibname gweather %major
%define develname %mklibname -d gweather
%define olddevelname %mklibname -d gnome-applets

Summary: GNOME Weather applet library
Name: %{name}
Version: %{version}
Release: %{release}
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
License: GPLv2+
Group: System/Libraries
Url: http://www.gnome.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libsoup-devel
BuildRequires: gtk+2-devel
BuildRequires: libGConf2-devel
BuildRequires: intltool
BuildRequires: libxml2-utils
Conflicts: gnome-applets < 2.21.3

%description
This is a library to provide Weather data to the GNOME panel applet.

%package -n %libname
Group: System/Libraries
Summary: GNOME Weather applet library
Requires: %name >= %version

%description -n %libname
This is a library to provide Weather data to the GNOME panel applet.

%package -n %develname
Group: Development/C
Summary: GNOME Weather applet library
Requires: %libname = %version
Provides: %name-devel = %version-%release
Obsoletes: %olddevelname < 2.21.3

%description -n %develname
This is a library to provide Weather data to the GNOME panel applet.

%prep
%setup -q

%build
%configure2_5x
%make 

%install
rm -rf %{buildroot} %name.lang
%makeinstall_std
%find_lang %name
for xmlfile in  %buildroot%_datadir/%name/Locations.*.xml; do
echo "%lang($(basename $xmlfile|sed -e s/Locations.// -e s/.xml//)) $(echo $xmlfile | sed s!%buildroot!!)" >> %name.lang
done

%clean
rm -rf %{buildroot}

%post
%post_install_gconf_schemas gweather
%preun
%preun_uninstall_gconf_schemas gweather

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif


%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS NEWS
%_sysconfdir/gconf/schemas/gweather.schemas
%dir %_datadir/%name
%_datadir/%name/locations.dtd
%_datadir/%name/Locations.xml

%files -n %libname
%defattr(-, root, root)
%_libdir/libgweather.so.%{major}*

%files -n %develname
%defattr(-, root, root)
%doc ChangeLog
%attr(644,root,root) %_libdir/lib*a
%_libdir/lib*.so
%_libdir/pkgconfig/*.pc
%_includedir/*
%_datadir/gtk-doc/html/%name
