# TODO:
# - internal portaudio crashes when only OSS is available on startup
# - use system portaudio (>= 19, but relies on local changes)
# - use system portSMF?
# - use system ffmpeg (libavcodec >= 51.53, libavformat >= 52.12, libavutil)
# - use system sbsms (>= 1.6.0, but relies on local changes)
# - use system libnyquist (if ever; currently it's a part of audacity project)
#
# Conditional build:
%bcond_with	ffmpeg		# build with ffmpeg support (currently audacity does not support ffmpeg 1.0)
%bcond_with	gtk3		# GTK+ 3.x instead of 2.x
#
Summary:	Audacity - manipulate digital audio waveforms
Summary(pl.UTF-8):	Audacity - narzędzie do obróbki plików dźwiękowych
Summary(ru.UTF-8):	Кроссплатформенный звуковой редактор
Name:		audacity
Version:	2.1.1
Release:	2
License:	GPL v2+
Group:		X11/Applications/Sound
#Source0Download: http://www.oldfoss.com/Audacity.html
Source0:	http://app.oldfoss.com:81/download/Audacity/%{name}-minsrc-%{version}.tar.xz
# Source0-md5:	9e37b1f5cde38d089a35febb904a9e39
Source1:	http://app.oldfoss.com:81/download/Audacity/%{name}-manual-%{version}.zip
# Source1-md5:	a4116a20798b827cd1e06e50c8099aa6
Source2:	%{name}.desktop
Source3:	%{name}-icon.png
Patch0:		%{name}-cast.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-no-macos.patch
URL:		http://audacityteam.org/
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	expat-devel >= 1.95
# libavcodec >= 51.53 libavformat >= 52.12 libavutil
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel >= 0.8.0}
BuildRequires:	flac-c++-devel >= 1.3.0
BuildRequires:	gettext-tools >= 0.18
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0}
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	hpklinux-devel >= 4.06
BuildRequires:	lame-libs-devel
BuildRequires:	libid3tag-devel >= 0.15.0b-2
BuildRequires:	libjpeg-devel
BuildRequires:	libmad-devel >= 0.14.2b-4
#BuildRequires:	libsbsms-devel >= 1.6.0
#BuildRequires:	libsbsms2-devel >= 2.0.2
BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libvorbis-devel >= 1:1.0
BuildRequires:	lilv-devel >= 0.16
BuildRequires:	lv2-devel
#BuildRequires:	portaudio-devel >= 19
BuildRequires:	pkgconfig
BuildRequires:	soundtouch-devel >= 1.3.0
BuildRequires:	soxr-devel >= 0.0.5
BuildRequires:	speex-devel
BuildRequires:	suil-devel >= 0.8.2
BuildRequires:	twolame-devel >= 0.3.9
BuildRequires:	udev-devel
BuildRequires:	unzip
BuildRequires:	vamp-devel >= 2.0
BuildRequires:	which
%{!?with_gtk3:BuildRequires:	wxGTK2-unicode-devel >= 2.8.0}
%{?with_gtk3:BuildRequires:	wxGTK3-unicode-devel >= 2.8.0}
Requires(post,postun):	shared-mime-info
Requires:	flac-c++ >= 1.3.0
Requires:	lame-libs
Requires:	libid3tag >= 0.15.0b-2
Requires:	libmad >= 0.14.2b-4
Requires:	libsndfile >= 1.0.0
Requires:	lilv
Requires:	soundtouch >= 1.3.0
%{?with_soxr:Requires:	soxr >= 0.0.5}
Requires:	suil
Requires:	twolame-libs >= 0.3.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Audacity is a program that lets you manipulate digital audio
waveforms. It imports many sound file formats, including WAV, AIFF,
AU, IRCAM, MP3, and Ogg Vorbis. It supports all common editing
operations such as Cut, Copy, and Paste, plus it will mix tracks and
let you apply plug-in effects to any part of a sound.

%description -l pl.UTF-8
Audacity to program obsługujący różne formaty plików audio. Obsługuje
WAV, AIFF, AU, IRCAM, MP3, oraz Ogg Vorbis. Program ten umożliwia
wykonywanie podstawowych czynności edycyjnych takich jak kasowanie,
wstawianie i miksowanie ścieżki dźwiękowej. Umożliwia także
wykonywanie dowolnych innych operacji poprzez system wtyczek.

%description -l ru.UTF-8
Audacity - это звуковой редактор, позволяющий работать с файлами в
форматах WAV, AIFF, AU, IRCAM, MP3 и Ogg Vorbis. В нем реализованы все
основные операции, такие как удаление, копирование, вставка,
микширование треков и применение эффектов, оформленных в виде
плагинов, к любой части звукового файла.

%package devel
Summary:	Header files for Audacity interfaces
Summary(pl.UTF-8):	Pliki nagłówkowe interfejsów Audacity
Group:		Development/Libraries
Requires:	libstdc++-devel
Requires:	wxWidgets-devel >= 2.8.0
# doesn't require base

%description devel
Header files for Audacity interfaces.

%description devel -l pl.UTF-8
Pliki nagłówkowe interfejsów Audacity.

%prep
%setup -q -n %{name}-minsrc-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# OPTIONAL_SUBDIRS are not included in tarball; allow autotools to work
%{__sed} -i '/SUBDIRS += \$(OPTIONAL_SUBDIRS)/d' lib-src/Makefile.am

%{__sed} -i 's/libmp3lame.so/libmp3lame.so.0/g' locale/*.po

%build
cd lib-src/portmixer
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
cd ../lib-widget-extra
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
cd ../FileDialog
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
cd ../portsmf
%{__aclocal} -I autotools/m4
%{__autoconf}
%{__automake}
cd ../..
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}

export WX_CONFIG=$(which wx-gtk%{?with_gtk3:3}%{!?with_gtk3:2}-unicode-config)
%configure \
	%{?with_gtk3:--enable-gtk3} \
	--with-ffmpeg%{!?with_ffmpeg:=no} \
	--with-help \
	--with-id3tag=system \
	--with-libmad=system \
	--with-libsndfile=system \
	--with-libflac=system \
	--with-sbsms=local \
	--with-soxr=system \
	--with-vorbis=system

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_PATH=$RPM_BUILD_ROOT

# install headers in standard location
install -d $RPM_BUILD_ROOT%{_includedir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/audacity/include/audacity $RPM_BUILD_ROOT%{_includedir}
rmdir $RPM_BUILD_ROOT%{_datadir}/audacity/include

cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}
%{__unzip} -qq -a %{SOURCE1} -d $RPM_BUILD_ROOT%{_datadir}/%{name}/help

# unify locale names
%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{ca_ES@valencia,ca@valencia}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{sr_RS,sr}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{sr_RS@latin,sr@latin}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{zh,zh_CN}

%{__rm} $RPM_BUILD_ROOT%{_datadir}/pixmaps/audacity.xpm
%{__rm} $RPM_BUILD_ROOT%{_datadir}/pixmaps/audacity16.xpm
%{__rm} $RPM_BUILD_ROOT%{_datadir}/pixmaps/audacity32.xpm
%{__rm} $RPM_BUILD_ROOT%{_datadir}/pixmaps/gnome-mime-application-x-audacity-project.xpm

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_mime_database

%postun
%update_mime_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/audacity
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/nyquist
%{_datadir}/%{name}/plug-ins
%{_datadir}/%{name}/EQDefaultCurves.xml
%doc %{_datadir}/%{name}/help
%{_mandir}/man1/audacity.1*
%{_desktopdir}/audacity.desktop
%{_pixmapsdir}/audacity-icon.png
%{_datadir}/appdata/audacity.appdata.xml
%{_datadir}/mime/packages/audacity.xml
%{_iconsdir}/hicolor/*/apps/audacity.png
%{_iconsdir}/hicolor/*/apps/audacity.svg

%files devel
%defattr(644,root,root,755)
%{_includedir}/audacity
