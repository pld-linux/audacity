Summary:	Audacity - manipulate digital audio waveforms
Summary(pl):	Audacity - narzкdzie do obrуbki plikуw dјwiкkowych
Summary(ru):	Кроссплатформенный звуковой редактор
Name:		audacity
Version:	1.1.1
%define	subv	3
Release:	2
License:	GPL
Vendor:		Dominic Mazzoni <dominic@minorninth.com>
Group:		X11/Applications/Sound
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/%{name}/%{name}-src-%{version}-%{subv}.tgz
# Source0-md5:	8fd7fc8ccc06b51ab3244a574dc0f3a9
Source1:	%{name}.desktop
Source2:	%{name}-icon.png
Patch0:		%{name}-system-expat.patch
Patch1:		%{name}-helpfile_location.patch
Patch2:		%{name}-not_require_lame-libs-devel.patch
Patch3:		%{name}-opt.patch
Patch4:		%{name}-segv.patch
URL:		http://audacity.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	expat-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libstdc++-devel
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
%setup -q -n %{name}-src-%{version}-%{subv}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__autoconf}
%configure \
	--with-id3tag=system \
	--with-libmad=system \
	--with-libsndfile=system \
	--with-vorbis=system

%{__make} \
	CCC="%{__cxx} -fno-exceptions -fno-rtti" \
	OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_applnkdir}/Multimedia,%{_pixmapsdir}}

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix}

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Multimedia
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

# not built in this version
#install audacity-help.htb $RPM_BUILD_ROOT%{_datadir}/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/audacity
%{_datadir}/%{name}
%{_mandir}/man1/*.1*
%{_applnkdir}/*/*
%{_pixmapsdir}/*
