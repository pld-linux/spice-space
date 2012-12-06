#
# Conditional build:
%bcond_with	slirp		# build with tunneling support (breaks qemu)
#
Summary:	SPICE virtualization solution
Summary(pl.UTF-8):	System wirtualizacji SPICE
# real package name (spice) is already occupied
Name:		spice-space
Version:	0.12.0
Release:	2
License:	LGPL v2.1+
Group:		Applications/Emulators
Source0:	http://spice-space.org/download/releases/spice-%{version}.tar.bz2
# Source0-md5:	12c6ea4938215f8f9f10d2925f7bec9b
Patch0:		spice-sh.patch
Patch1:		spice-link.patch
URL:		http://spice-space.org/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	celt051-devel >= 0.5.1.1
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	cyrus-sasl-devel >= 2
BuildRequires:	libcacard-devel >= 0.1.2
BuildRequires:	libjpeg-devel
%{?with_slirp:BuildRequires:	libslirp-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	pixman-devel >= 0.17.7
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	python-pyparsing
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	spice-protocol >= 0.10.1
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXinerama-devel >= 1.0
BuildRequires:	xorg-lib-libXrandr-devel >= 1.2
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	zlib-devel
ExclusiveArch:	%{ix86} %{x8664} arm
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
Requires:	pixman >= 0.17.7

%description -n spice-server-libs
SPICE server library.

%description -n spice-server-libs -l pl.UTF-8
Biblioteka serwera SPICE.

%package -n spice-server-devel
Summary:	Header files for SPICE server library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki serwera SPICE
Group:		Development/Libraries
Requires:	celt051-devel >= 0.5.1.1
%{?with_slirp:Requires:	libslirp-devel}
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
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-opengl \
	--enable-smartcard \
	%{?with_slirp:en}%{!?with_slirp:dis}able-tunnel
# --enable-gui		BR: CEGUI-devel >= 0.6.0 < 0.7.0

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

%files -n spice-client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/spicec
