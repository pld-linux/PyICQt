#
# TODO:
# - i suppose that workaround for python Twisted is also needed - goto workaround and think about it
# - description (both),

Summary:	Python ICQ jabber transport
Summary(pl.UTF-8):	Transport ICQ dla jabbera napisany w pythonie
Name:		PyICQt
Version:	0.8a
Release:	0.1
License:	GPL
Group:		Applications/Communications
Source0:	http://www.blathersource.org/download.php/pyicq-t/pyicq-t-%{version}.tar.gz
# Source0-md5:	eb44605d5f952759e3cba19815d367d2
Source1:	%{name}-config.xml
Source2:	%{name}.init
Source3:	pyicqt.sh
URL:		http://www.blathersource.org/
BuildRequires:	python
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-Imaging
Requires:	python-Twisted
Requires:	python-Twisted-ssl
Requires:	python-TwistedWeb
Requires:	python-TwistedWords
Requires:	python-TwistedXish
Requires:	python-pyOpenSSL
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl.UTF-8

%prep
%setup -q -n pyicq-t-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/pyicqt/src/{twistfix/words/{xish/,protocols/jabber/},legacy/services/,langs/,tlib/,services/,xdb/,web/},%{_var}/lib/pyicqt}
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jabber,/etc/rc.d/init.d}
install -d $RPM_BUILD_ROOT%{_datadir}/pyicqt/data/www/{css,images}
install -d $RPM_BUILD_ROOT%{_sbindir}
install src/twistfix/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/twistfix
install src/twistfix/words/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/twistfix/words
install src/twistfix/words/xish/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/twistfix/words/xish
install src/twistfix/words/protocols/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/twistfix/words/protocols
install src/twistfix/words/protocols/jabber/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/twistfix/words/protocols/jabber
install src/legacy/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/legacy
install src/legacy/services/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/legacy/services
install src/langs/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/langs
install src/tlib/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/tlib
install src/services/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/services
install src/xdb/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/xdb
install src/web/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src/web
install src/*.py $RPM_BUILD_ROOT%{_datadir}/pyicqt/src
install data/www/css/*.css $RPM_BUILD_ROOT%{_datadir}/pyicqt/data/www/css
install data/www/images/*.png $RPM_BUILD_ROOT%{_datadir}/pyicqt/data/www/images
install data/www/*.html $RPM_BUILD_ROOT%{_datadir}/pyicqt/data/www
install data/*.png $RPM_BUILD_ROOT%{_datadir}/pyicqt/data
install PyICQt.py $RPM_BUILD_ROOT%{_datadir}/pyicqt

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/jabber/PyICQt.xml
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/PyICQt
install %{SOURCE3} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

#ugly workaround (maybe fix in twisted words/xish package?)
%post
ln -s %{py_sitescriptdir}/twisted/words/ %{py_sitedir}/twisted/words
ln -s %{py_sitescriptdir}/twisted/xish/ %{py_sitedir}/twisted/xish

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

%postun
echo "Cleaing ugly workaround (%{py_sitedir}/twisted/{words,xish})"
rm -f %{py_sitedir}/twisted/words
rm -f %{py_sitedir}/twisted/xish

%files
%defattr(644,root,root,755)
%doc README NEWS AUTHORS ChangeLog
%dir %{_datadir}/pyicqt/src/twistfix
%{_datadir}/pyicqt/src/twistfix/*.py
%dir %{_datadir}/pyicqt/src/twistfix/words
%{_datadir}/pyicqt/src/twistfix/words/*.py
%dir %{_datadir}/pyicqt/src/twistfix/words/xish
%{_datadir}/pyicqt/src/twistfix/words/xish/*.py
%dir %{_datadir}/pyicqt/src/twistfix/words/protocols
%{_datadir}/pyicqt/src/twistfix/words/protocols/*.py
%dir %{_datadir}/pyicqt/src/twistfix/words/protocols/jabber
%{_datadir}/pyicqt/src/twistfix/words/protocols/jabber/*.py
%dir %{_datadir}/pyicqt/src/legacy
%{_datadir}/pyicqt/src/legacy/*.py
%dir %{_datadir}/pyicqt/src/legacy/services
%{_datadir}/pyicqt/src/legacy/services/*.py
%dir %{_datadir}/pyicqt/src/langs
%{_datadir}/pyicqt/src/langs/*.py
%dir %{_datadir}/pyicqt/src/tlib
%{_datadir}/pyicqt/src/tlib/*.py
%dir %{_datadir}/pyicqt/src/services
%{_datadir}/pyicqt/src/services/*.py
%dir %{_datadir}/pyicqt/src/xdb
%{_datadir}/pyicqt/src/xdb/*.py
%dir %{_datadir}/pyicqt/src/web
%{_datadir}/pyicqt/src/web/*.py
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
%attr(755,root,root) %{_sbindir}/*.sh
