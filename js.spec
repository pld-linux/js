#
# Conditional build:
%bcond_with	threads	# build thread-safe library (requires nspr)
%bcond_with	java	# with libjsj and lshell
#
%include        /usr/lib/rpm/macros.perl
Summary:	JavaScript Reference Implementation
Summary(pl):	Wzorcowa implementacja JavaScriptu
Name:		js
Version:	1.5
%define	rcver	rc6a
Release:	1.%{rcver}.1
Epoch:		1
License:	GPL or Netscape Public License 1.1
Group:		Libraries
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/%{name}-%{version}-%{rcver}.tar.gz
# Source0-md5:	25e1d1dd2674d85883391b6b42a7b02f
Patch0:		%{name}-makefile.patch
URL:		http://www.mozilla.org/js/
%{?with_java:BuildRequires:	jdk}
%{?with_threads:BuildRequires:	nspr-devel}
BuildRequires:	perl-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov
Conflicts:	njs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		classdir	%{_datadir}/java

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
Requires:	%{name} = %{epoch}:%{version}-%{release}
Conflicts:	njs-devel

%description devel
Header files for JavaScript reference library.

%description devel -l pl
Pliki nag³ówkowe do biblioteki JavaScript.

%package static
Summary:	Static JavaScript reference library
Summary(pl):	Statyczna biblioteka JavaScript
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Conflicts:	njs-static

%description static
Static version of JavaScript reference library.

%description static -l pl
Statyczna wersja biblioteki JavaScript.

%package java
Summary:	JavaScript LiveConnect Version 3 implementation
Summary(pl):	Implementacja JavaScript LiveConnect w wersji 3
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Conflicts:	mozilla
Conflicts:	mozilla-embedded

%description java
LiveConnect is a library that permits JavaScript and Java virtual
machines to interoperate. Specifically, it enables JavaScript to
access Java fields, invoke Java methods and enables Java to access
JavaScript object properties and evaluate arbitrary JavaScript.
LiveConnect was originally an integrated feature of both the Netscape
Navigator browser and Netscape's server-side JavaScript. Now, it is a
standalone library that can be embedded within other projects, such as
the Mozilla browser.

%description java -l pl
LiveConnect to biblioteka pozwalaj±ca na wspó³pracê maszyn wirtualnych
JavaScriptu i Javy. W szczególno¶ci pozwala z poziomu JavaScriptu na
dostêp do pól Javy, wywo³ywanie metod Javy oraz z poziomu Javy na
dostêp do sk³adowych obiektów JavaScriptu i wykonywanie dowolnego kodu
w JavaScripcie. LiveConnect oryginalnie by³ zintegrowan± czê¶ci±
przegl±darki Netscape Navigator oraz Netscape JavaScript dzia³aj±cego
po stronie serwera. Teraz jest to samodzielna biblioteka, któr± mo¿na
osadzaæ w innych projektach, takich jak przegl±darka Mozilla.

%package java-devel
Summary:	JavaScript LiveConnect 3 implementation header files
Summary(pl):	Pliki nag³ówkowe implementacji JavaScript LiveConnect 3
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Requires:	%{name}-java = %{epoch}:%{version}-%{release}

%description java-devel
JavaScript LiveConnect 3 implementation header files.

%description java-devel -l pl
Pliki nag³ówkowe implementacji JavaScript LiveConnect 3.

%package java-static
Summary:	JavaScript Live Connect 3 implementation static library
Summary(pl):	Biblioteka statyczna implementacji JavaScript LiveConnect 3
Group:		Development/Libraries
Requires:	%{name}-java-devel = %{epoch}:%{version}-%{release}

%description java-static
JavaScript Live Connect 3 implementation static library.

%description java-static -l pl
Biblioteka statyczna implementacji JavaScript LiveConnect 3.

%package -n perl-JS
Summary:	JS Perl module - interface to JavaScript
Summary(pl):	Modu³ Perla JS - interfejs do JavaScriptu
Group:		Development/Languages/Perl
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n perl-JS
JS Perl module allows calling JavaScript from Perl.

%description -n perl-JS -l pl
Modu³ Perla JS pozwalaj±cy na wywo³ywanie JavaScriptu z Perla.

%prep
%setup -q -n %{name}
%patch -p1

echo 'SONAME=libjs.so.0' >> src/Makefile.ref
echo 'SONAME=libjsj.so.0' >> src/liveconnect/Makefile.ref

%build
%{__make} -C src -f Makefile.ref \
	%{!?debug:BUILD_OPT=1} \
	OPTIMIZER="%{rpmcflags} -DHAVE_VA_COPY -DVA_COPY=va_copy" \
	JS_READLINE=1 \
	CC="%{__cc}" \
	MKSHLIB="%{__cc} -shared -Wl,-soname=\$(SONAME)" \
	%{?with_threads:JS_THREADSAFE=1} \
	%{?with_java:JS_LIVECONNECT=1 JDK=%{_libdir}/java}

# js segfaults when jsperl is compiled in
#	JS_PERLCONNECT=1

cd src/perlconnect
%{!?debug:BUILD_OPT=1} \
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make} \
	OPTIMIZE="%{rpmcflags}"

# no UNIX makefiles
# %{__make} -C jsd

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}/js,%{classdir}}

cd src
install Linux*/{js,jscpucfg} $RPM_BUILD_ROOT%{_bindir}
install Linux*/libjs.a $RPM_BUILD_ROOT%{_libdir}
install Linux*/libjs.so $RPM_BUILD_ROOT%{_libdir}/libjs.so.0.1.0
ln -sf libjs.so.0 $RPM_BUILD_ROOT%{_libdir}/libjs.so
install Linux*/jsautocfg.h $RPM_BUILD_ROOT%{_includedir}/js
install js.msg jsapi.h jsarray.h jsarena.h jsatom.h jsbit.h jsbool.h \
	jsclist.h jscntxt.h jscompat.h jsconfig.h jsdate.h jsdbgapi.h \
	jsdhash.h jsemit.h jsfun.h jsgc.h jshash.h jsinterp.h jslock.h \
	jslong.h jsmath.h jsnum.h jsobj.h jsopcode.tbl jsopcode.h jsosdep.h \
	jsotypes.h jsparse.h jsprf.h jsprvtd.h jspubtd.h jsregexp.h jsscan.h \
	jsscope.h jsscript.h jsstr.h jstypes.h jsutil.h jsxdrapi.h jsstddef.h \
	$RPM_BUILD_ROOT%{_includedir}/js

%if %{with java}
install liveconnect/Linux*/libjsj.a $RPM_BUILD_ROOT%{_libdir}
install liveconnect/Linux*/libjsj.so $RPM_BUILD_ROOT%{_libdir}/libjsj.so.0.1.0
ln -sf libjsj.so.0 $RPM_BUILD_ROOT%{_libdir}/libjsj.so
install liveconnect/Linux*/lcshell $RPM_BUILD_ROOT%{_bindir}
install liveconnect/classes/Linux*/*.jar $RPM_BUILD_ROOT%{classdir}
install liveconnect/{jsjava.h,nsI*.h,_jni/*.h} $RPM_BUILD_ROOT%{_includedir}/js
%endif

%{__make} -C perlconnect install \
	DESTDIR=$RPM_BUILD_ROOT

cp -f perlconnect/README.html README-perlconnect.html

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	java -p /sbin/ldconfig
%postun	java -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc src/README*.html
%attr(755,root,root) %{_bindir}/js*
%attr(755,root,root) %{_libdir}/libjs.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjs.so
%dir %{_includedir}/js
%{_includedir}/js/js.msg
%{_includedir}/js/jsopcode.tbl
%{_includedir}/js/js[!j]*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libjs.a

%if %{with java}
%files java
%defattr(644,root,root,755)
%doc src/liveconnect/README.html
%attr(755,root,root) %{_bindir}/lcshell
%attr(755,root,root) %{_libdir}/libjsj.so.*.*.*
%{classdir}/*.jar

%files java-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjsj.so
%{_includedir}/js/jsjava.h
%{_includedir}/js/n*.h

%files java-static
%defattr(644,root,root,755)
%{_libdir}/libjsj.a
%endif

%files -n perl-JS
%defattr(644,root,root,755)
%{perl_vendorarch}/JS.pm
%{perl_vendorarch}/jsperlbuild.pl
%dir %{perl_vendorarch}/auto/JS
%{perl_vendorarch}/auto/JS/JS.bs
%attr(755,root,root) %{perl_vendorarch}/auto/JS/JS.so
# unusable now (helper module for PerlConnect in libjs, which is not built)
#%%{perl_vendorarch}/PerlConnect.pm
