Summary:	Audacity - manipulate digital audio waveforms
Summary(pl):	Audacity - manipulacja plikami audio
Name:		audacity
Version:	0.98
Release:	1
License:	GPL
Vendor:		Dominic Mazzoni <dominic@minorninth.com>
Group:		X11/Applications/Multimedia
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-src-%{version}.tgz
Source1:	%{name}.desktop
Source2:	%{name}-icon.png
Patch0:		%{name}-dynamic_id3lib.patch
Patch1:		%{name}-helpfile_location.patch
Patch2:		%{name}-not_require_lame-libs-devel.patch
URL:		http://audacity.sourceforge.net/
Requires:	lame-libs
BuildRequires:	wxGTK-devel
BuildRequires:	mad-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtiff-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

%description
Audacity is a program that manipulates digital audio waveforms.
Supports wav, mp3 and ogg/vorbis.

%description -l pl
Audacity to program obs³uguj±cy ró¿ne formaty dzwiêku cyfrowego.
Obs³uguje .wav, .mp3 oraz ogg/vorbis.

%prep
%setup -q -n %{name}-src-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
autoconf
%configure \
	--with-vorbis \
	--with-libmad
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name},%{_applnkdir}/Multimedia,%{_pixmapsdir}}

install %{SOURCE1} $RPM_BUILD_ROOT/%{_applnkdir}/Multimedia
install %{SOURCE2} $RPM_BUILD_ROOT/%{_pixmapsdir}

install audacity $RPM_BUILD_ROOT%{_bindir}
install audacity-help.htb $RPM_BUILD_ROOT%{_datadir}/%{name}

gzip -9nf README.txt LICENSE.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt.gz LICENSE.txt.gz
%attr(755,root,root) %{_bindir}/audacity
%{_datadir}/%{name}/*
%{_applnkdir}/*/*
%{_pixmapsdir}/*
