%define name libgweather
%define version 2.22.0
%define release %mkrel 2
%define major 0
%define libname %mklibname gweather %major
%define develname %mklibname -d gweather
%define oldlibname %mklibname gnome-applets 0
%define olddevelname %mklibname -d gnome-applets

Summary: GNOME Weather applet library
Name: %{name}
Version: %{version}
Release: %{release}
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
# (fc) 2.22.0-2mdv fix i18n init
Patch0: libgweather-2.22.0-i18ninit.patch
License: GPL
Group: System/Libraries
Url: http://www.gnome.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gnome-vfs2-devel
BuildRequires: gtk+2-devel
BuildRequires: perl-XML-Parser
Conflicts: gnome-applets < 2.21.3

%description
This is a library to provide Weather data to the GNOME panel applet.

%package -n %libname
Group: System/Libraries
Summary: GNOME Weather applet library
#gw this is a split from gnome-applets
Obsoletes: %oldlibname < 2.21.3
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
%patch0 -p1 -b .i18ninit

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std
%find_lang %name

%clean
rm -rf %{buildroot}

%post
%post_install_gconf_schemas gweather
%preun
%preun_uninstall_gconf_schemas gweather

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig


%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS NEWS
%_sysconfdir/gconf/schemas/gweather.schemas
%_datadir/%name

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

