Summary:	Audacity - manipulate digital audio waveforms
Summary(pl):	Audacity - manipulacja plikami audio
Name:		audacity
Version:	0.97
Release:	1
License:	GPL
Vendor:		Dominic Mazzoni <dominic@minorninth.com>
Group:		X11/Applications/Multimedia
Group(de):	X11/Applikationen/Multimedia
Group(pl):	X11/Aplikacje/Multimedia
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-src-%{version}.tgz
URL:		http://audacity.sourceforge.net/
BuildRequires:	wxGTK-devel
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

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install audacity $RPM_BUILD_ROOT%{_bindir}

gzip -9nf README.txt LICENSE.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt.gz LICENSE.txt.gz
%attr(755,root,root) %{_bindir}/audacity
