# TODO:
# - internal portaudio crashes when only OSS is available on startup
# - use system portaudio (>= 19, but relies on local changes)
# - use system portSMF?
# - use system ffmpeg (libavcodec >= 51.53, libavformat >= 52.12)
# - use system sbsms (>= 1.6.0, but relies on local changes)
#
# Conditional build:
%bcond_with	libresample	# using libresample (default libsamplerate)
%bcond_with	ffmpeg		# build with ffmpeg support (currently audacity does not support ffmpeg 1.0)
#
Summary:	Audacity - manipulate digital audio waveforms
Summary(pl.UTF-8):	Audacity - narzędzie do obróbki plików dźwiękowych
Summary(ru.UTF-8):	Кроссплатформенный звуковой редактор
Name:		audacity
Version:	2.0.2
Release:	2
License:	GPL v2+
Group:		X11/Applications/Sound
#Source0Download: http://code.google.com/p/audacity/downloads/list
Source0:	http://audacity.googlecode.com/files/%{name}-minsrc-%{version}.tar.bz2
# Source0-md5:	c838bc4485b0af104a7f6d9c6955a284
# Link from http://manual.audacityteam.org/index.php?title=Main_Page
Source1:	http://audacity.googlecode.com/files/%{name}-manual-%{version}.zip
# Source1-md5:	2c80017f602dd6239ec3b6b0c25e68df
Source2:	%{name}.desktop
Source3:	%{name}-icon.png
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-no-macos.patch
# modified from http://audioscience.com/internet/download/drivers/released/v4/06/portaudio_asihpi_406.patch
Patch3:		portaudio_asihpi_406.patch
URL:		http://audacity.sourceforge.net/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	expat-devel >= 1.95
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel >= 0.8.0}
BuildRequires:	flac-c++-devel >= 1.2.0
BuildRequires:	gettext-devel
BuildRequires:	hpklinux-devel >= 4.06
BuildRequires:	libid3tag-devel >= 0.15.0b-2
BuildRequires:	libjpeg-devel
BuildRequires:	libmad-devel >= 0.14.2b-4
%{?with_libresample:BuildRequires:	libresample-devel >= 0.1.3}
%{!?with_libresample:BuildRequires:	libsamplerate-devel >= 0.1.2}
#BuildRequires:	libsbsms-devel >= 1.6.0
BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	libvorbis-devel >= 1:1.0
#BuildRequires:	portaudio-devel >= 19
BuildRequires:	pkgconfig
BuildRequires:	soundtouch-devel >= 1.3.0
BuildRequires:	speex-devel
BuildRequires:	twolame-devel >= 0.3.9
BuildRequires:	unzip
BuildRequires:	vamp-devel >= 2.0
BuildRequires:	which
BuildRequires:	wxGTK2-unicode-devel >= 2.8.0
Requires(post,postun):	shared-mime-info
Requires:	flac-c++ >= 1.2.0
Requires:	lame-libs
Requires:	libid3tag >= 0.15.0b-2
Requires:	libmad >= 0.14.2b-4
%{?with_libresample:Requires:	libresample >= 0.1.3}
%{!?with_libresample:Requires:	libsamplerate >= 0.1.2}
Requires:	libsndfile >= 1.0.0
Requires:	soundtouch >= 1.3.0
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

%prep
%setup -q -n %{name}-src-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
cd lib-src/portaudio-v19
%patch3 -p0
cd ../..

%{__sed} -i 's/libmp3lame.so/libmp3lame.so.0/g' locale/*.po

%build
cd lib-src/portmixer
%{__autoconf}
cd ../portsmf
%{__aclocal} -I autotools/m4
%{__autoconf}
cd ../..
%{__aclocal} -I m4
%{__autoconf}

export WX_CONFIG=$(which wx-gtk2-unicode-config)
%configure \
%if %{with libresample}
	--with-libresample=system \
%else
	--with-libresample=no \
	--with-libsamplerate=system \
%endif
	--with%{!?with_ffmpeg:out}-ffmpeg \
	--with-help \
	--with-id3tag=system \
	--with-libmad=system \
	--with-libsndfile=system \
	--with-libflac=system \
	--with-sbsms=local \
	--with-vorbis=system

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_PATH=$RPM_BUILD_ROOT

cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}
%{__unzip} -qq -a %{SOURCE1} -d $RPM_BUILD_ROOT%{_datadir}/%{name}/help

# unsupported
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/sr_RS*

mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{zh,zh_CN}
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

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
%{_datadir}/mime/packages/audacity.xml
%{_iconsdir}/hicolor/*/apps/audacity.png
%{_iconsdir}/hicolor/*/apps/audacity.svg
