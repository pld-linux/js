#
# Conditional build:
# _with_threads	- build thread-safe library (requires nspr)
# _with_java	- with libjsj and lshell
#
%include	/usr/lib/rpm/macros.perl
Summary:	JavaScript Reference Implementation
Summary(pl):	Wzorcowa implementacja JavaScriptu
Name:		js
Version:	1.5
%define	rcver	rc4a
Release:	0.%{rcver}
License:	GPL or Netscape Public License 1.1
Group:		Libraries
Source0:	http://ftp.mozilla.org/pub/js/%{name}-%{version}-%{rcver}.tar.gz
Patch0:		%{name}-makefile.patch
URL:		http://www.mozilla.org/js/
%{?_with_java:BuildRequires: jdk}
%{?_with_threads:BuildRequires:	nspr-devel}
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JavaScript Reference Implementation (codename SpiderMonkey). The
package contains JavaScript runtime (compiler, interpreter,
decompiler, garbage collector, atom manager, standard classes) and
small "shell" program that can be used interactively and with .js
files to run scripts.

%description -l pl
Wzorcowa implementacja JavaScriptu (o nazwie kodowej SpiderMonkey).
Pakiet zawiera ¶rodowisko uruchomieniowe (kompilator, interpreter,
dekompilator, od¶miecacz, standardowe klasy) i niewielk± pow³okê,
która mo¿e byæ u¿ywana interaktywnie lub z plikami .js do uruchamiania
skryptów.

%package devel
Summary:	Header files for JavaScript reference library
Summary(pl):	Pliki nag³ówkowe do biblioteki JavaScript
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for JavaScript reference library.

%description devel -l pl
Pliki nag³ówkowe do biblioteki JavaScript.

%package static
Summary:	Static JavaScript reference library
Summary(pl):	Statyczna biblioteka JavaScript
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static version of JavaScript reference library.

%description static -l pl
Statyczna wersja biblioteki JavaScript.

%package -n perl-JS
Summary:	JS perl module - interface to JavaScript
Summary(pl):	Modu³ perla JS - interfejs do JavaScriptu
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}

%description -n perl-JS
JS perl module allows calling JavaScript from Perl.

%description -n perl-JS -l pl
Modu³ perla JS pozwalaj±cy na wywo³ywanie JavaScriptu z Perla.

%prep
%setup -q -n %{name}
%patch -p1

%build
%{__make} -C src -f Makefile.ref \
	%{!?debug:BUILD_OPT=1} \
	OPTIMIZER="%{rpmcflags}" \
	JS_READLINE=1 \
	%{?_with_threads:JS_THREADSAFE=1} \
	%{?_with_java:JS_LIVECONNECT=1 JDK=/usr/lib/java}

# js segfaults when jsperl is compiled in
#	JS_PERLCONNECT=1

cd src/perlconnect
%{!?debug:BUILD_OPT=1} perl Makefile.PL

%{__make} \
	OPTIMIZE="%{rpmcflags}"

# no UNIX makefiles
# %{__make} -C jsd

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}/js}

cd src
install Linux*/{js,jscpucfg} $RPM_BUILD_ROOT%{_bindir}
install Linux*/libjs.{a,so} $RPM_BUILD_ROOT%{_libdir}
install Linux*/jsautocfg.h $RPM_BUILD_ROOT%{_includedir}/js
install js.msg jsapi.h jsarray.h jsarena.h jsatom.h jsbit.h jsbool.h \
	jsclist.h jscntxt.h jscompat.h jsconfig.h jsdate.h jsdbgapi.h \
	jsdhash.h jsemit.h jsfun.h jsgc.h jshash.h jsinterp.h jslock.h \
	jslong.h jsmath.h jsnum.h jsobj.h jsopcode.tbl jsopcode.h jsosdep.h \
	jsotypes.h jsparse.h jsprf.h jsprvtd.h jspubtd.h jsregexp.h jsscan.h \
	jsscope.h jsscript.h jsstr.h jstypes.h jsutil.h jsxdrapi.h jsstddef.h \
	$RPM_BUILD_ROOT%{_includedir}/js

%{?_with_java:install liveconnect/Linux*/libjsj.{a,so} $RPM_BUILD_ROOT%{_libdir}}
%{?_with_java:install liveconnect/Linux*/lcshell $RPM_BUILD_ROOT%{_bindir}}
%{?_with_java:install liveconnect/jsjava.h $RPM_BUILD_ROOT%{_includedir}/js}
%{?_with_java:install liveconnect/nsI*.h $RPM_BUILD_ROOT%{_includedir}/js}
%{?_with_java:install liveconnect/_jni/*.h $RPM_BUILD_ROOT%{_includedir}/js}

cd perlconnect
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd ..
%{?_with_java:mv -f liveconnect/README.html README-liveconnect.html}
mv -f perlconnect/README.html README-perlconnect.html

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc src/README*.html
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/js

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n perl-JS
%defattr(644,root,root,755)
%{perl_sitearch}/JS.pm
%{perl_sitearch}/jsperlbuild.pl
%dir %{perl_sitearch}/auto/JS
%{perl_sitearch}/auto/JS/JS.bs
%attr(755,root,root) %{perl_sitearch}/auto/JS/JS.so
# unusable now (helper module for PerlConnect in libjs, which is not built)
#%{perl_sitearch}/PerlConnect.pm
