Summary:	Python ICQ Jabber transport
Summary(pl.UTF-8):	Transport ICQ dla Jabbera napisany w Pythonie
Name:		PyICQt
Version:	0.8.1.5
Release:	1
License:	GPL v2
Group:		Applications/Communications
Source0:	http://pyicqt.googlecode.com/files/pyicqt-%{version}.tar.gz
# Source0-md5:	d1c544f82ed416bbe987a5e419820fa8
Source1:	%{name}-config.xml
Source2:	%{name}.init
URL:		http://www.blathersource.org/
BuildRequires:	python
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-PIL
Requires:	python-TwistedCore
Requires:	python-TwistedCore-ssl
Requires:	python-TwistedWeb
Requires:	python-TwistedWords >= 8.0.0
Requires:	python-pyOpenSSL
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python ICQ Jabber transport.

%description -l pl.UTF-8
Transport ICQ dla Jabbera napisany w Pythonie.

%prep
%setup -q -n pyicqt-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/pyicqt/src/{chardet_utf,langs,legacy/services,services,tlib,web,xdb},%{_var}/lib/pyicqt}
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jabber,/etc/rc.d/init.d}
install -d $RPM_BUILD_ROOT%{_datadir}/pyicqt/data/www/{css,images}
install src/chardet_utf/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/chardet_utf
install src/langs/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/langs
install src/legacy/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/legacy
install src/legacy/services/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/legacy/services
install src/services/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/services
install src/tlib/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/tlib
install src/web/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/web
install src/xdb/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/xdb
install src/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src
install data/www/css/*.css $RPM_BUILD_ROOT%{_datadir}/pyicqt/data/www/css
install data/www/images/*.png $RPM_BUILD_ROOT%{_datadir}/pyicqt/data/www/images
install data/www/*.html $RPM_BUILD_ROOT%{_datadir}/pyicqt/data/www
install data/*.png $RPM_BUILD_ROOT%{_datadir}/pyicqt/data
install PyICQt.py $RPM_BUILD_ROOT%{_datadir}/pyicqt

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/jabber/PyICQt.xml
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/PyICQt

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/jabber/secret ] ; then
	SECRET=`cat %{_sysconfdir}/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in PyICQt.xml..."
		%{__sed} -i -e "s/>secret</>$SECRET</" /etc/jabber/PyICQt.xml
	fi
fi
/sbin/chkconfig --add PyICQt
%service PyICQt restart "Jabber ICQ transport"

%preun
if [ "$1" = "0" ]; then
	%service PyICQt stop
	/sbin/chkconfig --del PyICQt
fi

%files
%defattr(644,root,root,755)
%doc README NEWS AUTHORS ChangeLog
%dir %{_datadir}/pyicqt/src/chardet_utf
%{_datadir}/pyicqt/src/chardet_utf/*.py
%dir %{_datadir}/pyicqt/src/langs
%{_datadir}/pyicqt/src/langs/*.py
%dir %{_datadir}/pyicqt/src/legacy
%{_datadir}/pyicqt/src/legacy/*.py
%dir %{_datadir}/pyicqt/src/legacy/services
%{_datadir}/pyicqt/src/legacy/services/*.py
%dir %{_datadir}/pyicqt/src/services
%{_datadir}/pyicqt/src/services/*.py
%dir %{_datadir}/pyicqt/src/tlib
%{_datadir}/pyicqt/src/tlib/*.py
%dir %{_datadir}/pyicqt/src/web
%{_datadir}/pyicqt/src/web/*.py
%dir %{_datadir}/pyicqt/src/xdb
%{_datadir}/pyicqt/src/xdb/*.py
%dir %{_datadir}/pyicqt/src
%{_datadir}/pyicqt/src/*.py
%dir %{_datadir}/pyicqt/data/www/images
%{_datadir}/pyicqt/data/www/images/*.png
%dir %{_datadir}/pyicqt/data/www/css
%{_datadir}/pyicqt/data/www/css/*.css
%dir %{_datadir}/pyicqt/data/www
%{_datadir}/pyicqt/data/www/*.html
%dir %{_datadir}/pyicqt/data
%{_datadir}/pyicqt/data/*.png
%dir %{_datadir}/pyicqt
%attr(755,root,root) %{_datadir}/pyicqt/*.py
%dir %{_var}/lib/pyicqt
%attr(754,root,root) /etc/rc.d/init.d/PyICQt
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/PyICQt.xml
