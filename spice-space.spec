#
# Conditional build:
%bcond_without	opengl	# OpenGL support
#
Summary:	SPICE virtualization solution
Summary(pl.UTF-8):	System wirtualizacji SPICE
# real package name (spice) is already occupied
Name:		spice-space
# NOTE: 0.13.x is unstable (see DEVEL branch for it)
Version:	0.14.0
Release:	2
License:	LGPL v2.1+
Group:		Applications/Emulators
Source0:	https://www.spice-space.org/download/releases/spice-%{version}.tar.bz2
# Source0-md5:	6622aa7dfb5cd026a4d0d7e659216d26
Patch0:		spice-am.patch
URL:		https://www.spice-space.org/
%{?with_opengl:BuildRequires:	OpenGL-devel}
%{?with_opengl:BuildRequires:	OpenGL-GLU-devel}
BuildRequires:	alsa-lib-devel
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	celt051-devel >= 0.5.1.1
BuildRequires:	cyrus-sasl-devel >= 2
BuildRequires:	gcc >= 5:3.2
BuildRequires:	glib2-devel >= 1:2.28
BuildRequires:	libcacard-devel >= 0.1.2
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	lz4-devel
BuildRequires:	openssl-devel
BuildRequires:	opus-devel >= 0.9.14
BuildRequires:	pixman-devel >= 0.17.7
BuildRequires:	pkgconfig
BuildRequires:	python >= 2
BuildRequires:	python-pyparsing
BuildRequires:	python-six
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	spice-protocol >= 0.12.13
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXinerama-devel >= 1.0
BuildRequires:	xorg-lib-libXrandr-devel >= 1.2
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	zlib-devel
ExclusiveArch:	%{ix86} %{x8664} x32 arm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Spice is an open remote computing solution, providing client access to
remote machine display and devices (e.g., keyboard, mouse, audio).
Spice achieves a user experience similar to an interaction with a
local machine, while trying to offload most of the intensive CPU and
GPU tasks to the client. Spice is suitable for both LAN and WAN usage,
without compromising on the user experience.

%description -l pl.UTF-8
Spice to rozwiązanie do zdalnych obliczeń, zapewniające dostęp
kliencki ekranu i urządzeń zdalnej maszyny (klawiatury, myszy,
dźwięku). Daje użytkownikowi wrażenie podobne do pracy lokalnej, ale
próbuje większość zadań wykorzystujących intensywnie CPU i GPU zrzucić
na klienta. Nadaje się do pracy w sieciach LAN i WAN, bez większych
poświęceń ze strony doznań użytkownika.

%package -n spice-server-libs
Summary:	SPICE server library
Summary(pl.UTF-8):	Biblioteka serwera SPICE
Group:		Libraries
Requires:	celt051 >= 0.5.1.1
Requires:	opus >= 0.9.14
Requires:	glib2 >= 1:2.22
Requires:	pixman >= 0.17.7
Obsoletes:	spice-client

%description -n spice-server-libs
SPICE server library.

%description -n spice-server-libs -l pl.UTF-8
Biblioteka serwera SPICE.

%package -n spice-server-devel
Summary:	Header files for SPICE server library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki serwera SPICE
Group:		Development/Libraries
Requires:	celt051-devel >= 0.5.1.1
Requires:	glib2-devel >= 1:2.22
Requires:	openssl-devel
Requires:	pixman-devel >= 0.17.7
Requires:	spice-server-libs = %{version}-%{release}

%description -n spice-server-devel
Header files for SPICE server library.

%description -n spice-server-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki serwera SPICE.

%package -n spice-server-static
Summary:	Static SPICE server library
Summary(pl.UTF-8):	Statyczna biblioteka serwera SPICE
Group:		Development/Libraries
Requires:	spice-server-devel = %{version}-%{release}

%description -n spice-server-static
Static SPICE server library.

%description -n spice-server-static -l pl.UTF-8
Statyczna biblioteka serwera SPICE.

%package -n spice-client
Summary:	SPICE client for X11
Summary(pl.UTF-8):	Klient SPICE dla X11
Group:		X11/Applications
Requires:	celt051 >= 0.5.1.1
Requires:	libcacard >= 0.1.2
Requires:	opus >= 0.9.14
Requires:	pixman >= 0.17.7
Requires:	xorg-lib-libXrandr >= 1.2
Requires:	xorg-lib-libXinerama >= 1.0

%description -n spice-client
SPICE client for X11.

%description -n spice-client -l pl.UTF-8
Klient SPICE dla X11.

%prep
%setup -q -n spice-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd spice-common
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd ..
%configure \
	--disable-silent-rules \
	--enable-client \
	--enable-lz4 \
	%{?with_opengl:--enable-opengl} \
	--enable-smartcard \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libspice-server.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n spice-server-libs -p /sbin/ldconfig
%postun	-n spice-server-libs -p /sbin/ldconfig

%files -n spice-server-libs
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_libdir}/libspice-server.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspice-server.so.1

%files -n spice-server-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libspice-server.so
%{_includedir}/spice-server
%{_pkgconfigdir}/spice-server.pc

%files -n spice-server-static
%defattr(644,root,root,755)
%{_libdir}/libspice-server.a
