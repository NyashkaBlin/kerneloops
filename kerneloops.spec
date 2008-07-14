%bcond_without	tests
Summary:	Tool to automatically collect and submit kernel crash signatures
Name:		kerneloops
Version:	0.11
Release:	1.1
License:	GPL v2
Group:		Base/Kernel
URL:		http://www.kerneloops.org
Source0:	http://www.kerneloops.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	a0daa9437f0638912a91afe66f51545b
Source1:	%{name}.init
BuildRequires:	curl-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libnotify-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the tools to collect kernel crash signatures,
and to submit them to the kerneloops.org website where the kernel
crash signatures get collected and grouped for presentation to the
Linux kernel developers.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%{?with_tests:%{__make} tests}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d/

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc Changelog
%attr(755,root,root) %{_sbindir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kerneloops.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
/etc/dbus-1/system.d/kerneloops.dbus
%{_sysconfdir}/xdg/autostart/kerneloops-applet.desktop
%{_datadir}/kerneloops
%attr(755,root,root) %{_bindir}/kerneloops-applet
%{_mandir}/man8/kerneloops.8*
