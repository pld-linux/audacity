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
%define		_mandir		/usr/man

%description
Audacity is a program that manipulates digital audio waveforms.

%description -l pl
Audacity to program obs³uguj±cy ró¿ne formaty dzwiêku cyfrowego.
Obs³uguje .wav, .mp3 oraz ogg/vorbis

%prep
%setup -q -n %{name}-src-%{version}
echo --------------------------- SETUP DONE ---------------------------

%build
./configure --prefix=%{_prefix} --mandir=%{_mandir}
%{__make}
echo --------------------------- BUILD DONE ---------------------------

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/doc/audacity
mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin
cp README.txt 	$RPM_BUILD_ROOT%{_prefix}/share/doc/audacity/README.txt
cp LICENSE.txt 	$RPM_BUILD_ROOT%{_prefix}/share/doc/audacity/LICENSE.txt
cp audacity 	$RPM_BUILD_ROOT%{_prefix}/bin/audacity
echo --------------------------- INSTALL DONE ---------------------------

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt LICENSE.txt
%attr(755,root,root) /usr/X11R6/bin/audacity
