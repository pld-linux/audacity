Summary:	Audacity - manipulate digital audio waveforms
Summary(pl):	Audacity - narzкdzie do obrуbki plikуw dјwiкkowych
Summary(ru):	Кроссплатформенный звуковой редактор
Name:		audacity
Version:	1.0.0
Release:	2
License:	GPL
Vendor:		Dominic Mazzoni <dominic@minorninth.com>
Group:		X11/Applications/Sound
Source0:	http://dl.sourceforge.net/%{name}/%{name}-src-%{version}.tgz
# Source0-md5:	6711813f16c3d64e63209cb355191af6
Source1:	%{name}.desktop
Source2:	%{name}-icon.png
Patch0:		%{name}-dynamic_id3lib.patch
Patch1:		%{name}-helpfile_location.patch
Patch2:		%{name}-not_require_lame-libs-devel.patch
URL:		http://audacity.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	id3lib-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libvorbis-devel >= 1:1.0
BuildRequires:	mad-devel
BuildRequires:	wxGTK-devel >= 2.3.2-10
Requires:	lame-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

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

%build
%{__autoconf}
%configure \
	--with-id3=system \
	--with-libmad=system \
	--with-vorbis=system

%{__make} CCC="%{__cxx} -fno-exceptions -fno-rtti"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name},%{_applnkdir}/Multimedia,%{_pixmapsdir}}

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Multimedia
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

install audacity $RPM_BUILD_ROOT%{_bindir}
install audacity-help.htb $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/audacity
%{_datadir}/%{name}
%{_applnkdir}/*/*
%{_pixmapsdir}/*
