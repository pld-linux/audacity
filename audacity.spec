Summary:	Audacity - manipulate digital audio waveforms
Summary(pl):	Audacity - narzкdzie do obrуbki plikуw dјwiкkowych
Summary(ru):	Кроссплатформенный звуковой редактор
Name:		audacity
Version:	1.2.4b
Release:	1
License:	GPL
Vendor:		Dominic Mazzoni <dominic@minorninth.com>
Group:		X11/Applications/Sound
Source0:	http://dl.sourceforge.net/audacity/%{name}-src-%{version}.tar.gz
# Source0-md5:	37df5b6119302f7ab77ca16d25311756
Source1:	%{name}.desktop
Source2:	%{name}-icon.png
Patch0:		%{name}-system-expat.patch
Patch1:		%{name}-not_require_lame-libs-devel.patch
Patch2:		%{name}-opt.patch
Patch3:		%{name}-types.patch
URL:		http://audacity.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	fftw-devel >= 2.1.4
BuildRequires:	flac-devel
BuildRequires:	gettext-devel
BuildRequires:	libid3tag-devel >= 0.15.0b-2
BuildRequires:	libjpeg-devel
BuildRequires:	libmad-devel >= 0.14.2b-4
BuildRequires:	libsamplerate-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libvorbis-devel >= 1:1.0
BuildRequires:	which
BuildRequires:	wxGTK2-devel >= 2.6.0
BuildRequires:	zip
Requires:	lame-libs
Requires:	libid3tag >= 0.15.0b-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Audacity is a program that lets you manipulate digital audio
waveforms. It imports many sound file formats, including WAV, AIFF,
AU, IRCAM, MP3, and Ogg Vorbis. It supports all common editing
operations such as Cut, Copy, and Paste, plus it will mix tracks and
let you apply plug-in effects to any part of a sound.

%description -l pl
Audacity to program obsіuguj±cy rуїne formaty plikуw audio. Obsіuguje
WAV, AIFF, AU, IRCAM, MP3, oraz Ogg Vorbis. Program ten umoїliwia
wykonywanie podstawowych czynno¶ci edycyjnych takich jak kasowanie,
wstawianie i miksowanie ¶cieїki dјwiкkowej. Umoїliwia takїe
wykonywanie dowolnych innych operacji poprzez system wtyczek.

%description -l ru
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
%patch3 -p1

%build
cp -f /usr/share/automake/config.sub .
cp -f /usr/share/automake/config.sub lib-src/soundtouch/config
%{__autoconf}
export WX_CONFIG="`which wx-gtk2-ansi-config`"
%configure \
	--with-help \
	--with-id3tag=system \
	--with-libmad=system \
	--with-libsamplerate=system \
	--with-libsndfile=system \
	--with-libflac=system \
	--with-vorbis=system

%{__make} \
	OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_PATH=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{zh,zh_CN}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/audacity
%{_datadir}/%{name}
%{_mandir}/man1/*.1*
%{_desktopdir}/*
%{_pixmapsdir}/*
