#
# Conditional build:
%bcond_without	opengl		# OpenGL support
%bcond_without	static_libs	# static library
#
Summary:	SPICE virtualization solution
Summary(pl.UTF-8):	System wirtualizacji SPICE
# real package name (spice) is already occupied
Name:		spice-space
# NOTE: 0.odd.x versions are unstable
Version:	0.15.2
Release:	1
License:	LGPL v2.1+
Group:		Applications/Emulators
Source0:	https://www.spice-space.org/download/releases/spice-server/spice-%{version}.tar.bz2
# Source0-md5:	1de1e9157a1e2396884017978e7cf086
Patch0:		python3.patch
URL:		https://www.spice-space.org/
%{?with_opengl:BuildRequires:	OpenGL-GLU-devel}
%{?with_opengl:BuildRequires:	OpenGL-devel}
BuildRequires:	alsa-lib-devel
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.63
BuildRequires:	autoconf-archive
BuildRequires:	automake >= 1:1.11
BuildRequires:	cyrus-sasl-devel >= 2
BuildRequires:	gcc >= 5:4.0
BuildRequires:	gdk-pixbuf2-devel >= 2.26
BuildRequires:	glib2-devel >= 1:2.38
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
BuildRequires:	libcacard-devel >= 2.5.1
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel >= 6:4.8.1
BuildRequires:	libtool >= 2:2
BuildRequires:	lz4-devel >= 129
BuildRequires:	openssl-devel >= 1.0.0
BuildRequires:	opus-devel >= 1.0.0
BuildRequires:	orc-devel >= 0.4
BuildRequires:	pixman-devel >= 0.17.7
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	python3-pyparsing
BuildRequires:	python3-six
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	spice-protocol >= 0.14.3
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXinerama-devel >= 1.0
BuildRequires:	xorg-lib-libXrandr-devel >= 1.2
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	zlib-devel
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
Requires:	glib2 >= 1:2.38
Requires:	openssl >= 1.0.0
Requires:	opus >= 1.0.0
Requires:	pixman >= 0.17.7
Obsoletes:	spice-client < 0.12.6

%description -n spice-server-libs
SPICE server library.

%description -n spice-server-libs -l pl.UTF-8
Biblioteka serwera SPICE.

%package -n spice-server-devel
Summary:	Header files for SPICE server library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki serwera SPICE
Group:		Development/Libraries
Requires:	glib2-devel >= 1:2.38
Requires:	libcacard-devel >= 2.5.1
Requires:	openssl-devel >= 1.0.0
Requires:	pixman-devel >= 0.17.7
Requires:	spice-protocol >= 0.14.0
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

%prep
%setup -q -n spice-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd subprojects/spice-common
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd ../..
%configure \
	--disable-silent-rules \
	--enable-lz4 \
	%{?with_opengl:--enable-opengl} \
	--enable-smartcard \
	%{?with_static_libs:--enable-static}

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
%doc AUTHORS CHANGELOG.md README
%attr(755,root,root) %{_libdir}/libspice-server.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspice-server.so.1

%files -n spice-server-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libspice-server.so
%{_includedir}/spice-server
%{_pkgconfigdir}/spice-server.pc

%if %{with static_libs}
%files -n spice-server-static
%defattr(644,root,root,755)
%{_libdir}/libspice-server.a
%endif
