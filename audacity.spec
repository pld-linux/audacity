# TODO:
# - internal portaudio crashes when only OSS is available on startup
# - use system portaudio (>= 19, but relies on local changes)
# - use system portSMF?
# - use system ffmpeg (libavcodec >= 51.53, libavformat >= 52.12, libavutil)
# - use system sbsms (>= 1.6.0, but relies on local changes)
# - use system libnyquist (if ever; currently it's a part of audacity project)
#
# Conditional build:
%bcond_without	ffmpeg		# build without ffmpeg support
%bcond_with	gtk3		# GTK+ 3.x instead of 2.x (not fully supported)
%bcond_without	mmx		# MMX instructions
%bcond_without	sse		# SSE instructions
%bcond_without	sse2		# SSE2 instructions
#
%ifnarch %{x8664} x32 pentium2 pentium3 pentium4 athlon
%undefine	with_mmx
%endif
%ifnarch %{x8664} x32 pentium3 pentium4
%undefine	with_sse
%endif
%ifnarch %{x8664} x32 pentium4
%undefine	with_sse2
%endif

Summary:	Audacity - manipulate digital audio waveforms
Summary(pl.UTF-8):	Audacity - narzędzie do obróbki plików dźwiękowych
Summary(ru.UTF-8):	Кроссплатформенный звуковой редактор
Name:		audacity
Version:	2.4.2
Release:	1
License:	GPL v2+
Group:		X11/Applications/Sound
#Source0Download: http://www.fosshub.com/Audacity.html
Source0:	%{name}-minsrc-%{version}.tar.xz
# Source0-md5:	4a34c1c66f69f1fedc400c71d5155ea8
Source1:	%{name}-manual-%{version}.zip
# Source1-md5:	084830de81c157d229089338a594baab
Patch0:		%{name}-opt.patch
Patch1:		%{name}-no-macos.patch
Patch2:		%{name}-desktop.patch
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
BuildRequires:	hpklinux-devel >= 4.06
BuildRequires:	jack-audio-connection-kit-devel
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
BuildRequires:	nasm
BuildRequires:	pkgconfig
#BuildRequires:	portaudio-devel >= 19
BuildRequires:	rpmbuild(macros) >= 1.742
BuildRequires:	soundtouch-devel >= 1.3.0
BuildRequires:	soxr-devel >= 0.0.5
BuildRequires:	speex-devel
BuildRequires:	suil-devel >= 0.8.2
BuildRequires:	tar >= 1:1.22
BuildRequires:	twolame-devel >= 0.3.9
BuildRequires:	udev-devel
BuildRequires:	unzip
BuildRequires:	vamp-devel >= 2.0
BuildRequires:	which
%{!?with_gtk3:BuildRequires:	wxGTK2-unicode-devel >= 3.0.0}
%{?with_gtk3:BuildRequires:	wxGTK3-unicode-devel >= 3.0.0}
BuildRequires:	xz
Requires(post,postun):	shared-mime-info
Requires:	flac-c++ >= 1.3.0
# dlopened
Requires:	lame-libs
Requires:	libid3tag >= 0.15.0b-2
Requires:	libmad >= 0.14.2b-4
Requires:	libsndfile >= 1.0.0
Requires:	lilv >= 0.16
Requires:	soundtouch >= 1.3.0
Requires:	soxr >= 0.0.5
Requires:	suil >= 0.8.2
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
%setup -q -n %{name}-minsrc-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__sed} -i 's/libmp3lame.so/libmp3lame.so.0/g' locale/*.po

# Audacity's cmake can't find libmp3lame without a .pc file
# This is a temporary workaround.
if ! test -e %{_pkgconfigdir}/lame.pc
then
echo "creating lame.pc"
cat << EOF > lame.pc
prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/lame

Name: mp3lame
Description: encoder that converts audio to the MP3 file format.
Version: 3.100
Libs: -L${libdir} -lmp3lame
Cflags: -I${includedir}
EOF
fi

%build
if ! test -e %{_pkgconfigdir}/lame.pc
then
export PKG_CONFIG_PATH="`echo $PWD`:%{_pkgconfigdir}"
fi

mkdir -p build
cd build
%cmake .. \
	%{cmake_on_off mmx HAVE_MMX} \
	%{cmake_on_off sse HAVE_SSE} \
	%{cmake_on_off sse2 HAVE_SSE2} \
	-DwxWidgets_CONFIG_EXECUTABLE:FILEPATH=$(which wx-gtk%{?with_gtk3:3}%{!?with_gtk3:2}-unicode-config) \
	%{!?with_ffmpeg:-Daudacity_use_ffmpeg:STRING=off} \
	-DCMAKE_BUILD_TYPE=Release

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_PATH=$RPM_BUILD_ROOT
cd ..

%{__unzip} -qq -a %{SOURCE1} -d $RPM_BUILD_ROOT%{_datadir}/%{name}/help

# unify locale names
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{ca_ES@valencia,ca@valencia}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{pt_PT,pt}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{sr_RS,sr}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{sr_RS@latin,sr@latin}

# remove unsupported locale
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/eu_ES

%{__rm} $RPM_BUILD_ROOT%{_pixmapsdir}/audacity.xpm
%{__rm} $RPM_BUILD_ROOT%{_pixmapsdir}/audacity16.xpm
%{__rm} $RPM_BUILD_ROOT%{_pixmapsdir}/audacity32.xpm
%{__rm} $RPM_BUILD_ROOT%{_pixmapsdir}/gnome-mime-application-x-audacity-project.xpm

%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/README.txt
%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/LICENSE.txt
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{16x16,22x22,24x24,32x32,48x48}/apps
%{__mv} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{16x16,16x16/apps}/%{name}.png
%{__mv} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{22x22,22x22/apps}/%{name}.png
%{__mv} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{24x24,24x24/apps}/%{name}.png
%{__mv} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{32x32,32x32/apps}/%{name}.png
%{__mv} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{48x48,48x48/apps}/%{name}.png


%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_mime_database

%postun
%update_mime_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.txt LICENSE.txt
%attr(755,root,root) %{_bindir}/audacity
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/modules
%attr(755,root,root) %{_datadir}/%{name}/modules/mod-script-pipe.so
%{_datadir}/%{name}/nyquist
%{_datadir}/%{name}/plug-ins
%{_datadir}/%{name}/EQDefaultCurves.xml
%doc %{_datadir}/%{name}/help
%{_mandir}/man1/audacity.1*
%{_desktopdir}/audacity.desktop
%{_datadir}/appdata/audacity.appdata.xml
%{_datadir}/mime/packages/audacity.xml
%{_iconsdir}/hicolor/*/apps/*.*
