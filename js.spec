#
# Conditional build:
# _with_threads	- build thread-safe library (requires nspr)
# _with_java	- with libjsj and lshell
#
%include        /usr/lib/rpm/macros.perl
Summary:	JavaScript Reference Implementation
Summary(pl):	Wzorcowa implementacja JavaScriptu
Name:		js
Version:	1.5
%define	rcver	rc5a
Release:	0.%{rcver}.1
License:	GPL or Netscape Public License 1.1
Group:		Libraries
Source0:	http://ftp.mozilla.org/pub/js/%{name}-%{version}-%{rcver}.tar.gz
# Source0-md5:	001fae2f953c2bbc0b495ee0823a3539
Patch0:		%{name}-makefile.patch
URL:		http://www.mozilla.org/js/
%{?_with_java:BuildRequires:	jdk}
%{?_with_threads:BuildRequires:	nspr-devel}
BuildRequires:	perl-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov
BuildRequires:	kernel-headers
Conflicts:	njs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		classdir	/usr/share/java

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
Conflicts:	njs-devel

%description devel
Header files for JavaScript reference library.

%description devel -l pl
Pliki nag³ówkowe do biblioteki JavaScript.

%package static
Summary:	Static JavaScript reference library
Summary(pl):	Statyczna biblioteka JavaScript
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}
Conflicts:	njs-static

%description static
Static version of JavaScript reference library.

%description static -l pl
Statyczna wersja biblioteki JavaScript.

%package java
Summary:	JavaScript LiveConnect Version 3 implementation
Summary(pl):	Implementacja JavaScript LiveConnect w wersji 3
Group:		Libraries
Requires:	%{name} = %{version}
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
Requires:	%{name}-devel = %{version}
Requires:	%{name}-java = %{version}

%description java-devel
JavaScript LiveConnect 3 implementation header files.

%description java-devel -l pl
Pliki nag³ówkowe implementacji JavaScript LiveConnect 3.

%package java-static
Summary:	JavaScript Live Connect 3 implementation static library
Summary(pl):	Biblioteka statyczna implementacji JavaScript LiveConnect 3
Group:		Development/Libraries
Requires:	%{name}-java-devel = %{version}

%description java-static
JavaScript Live Connect 3 implementation static library.

%description java-static -l pl
Biblioteka statyczna implementacji JavaScript LiveConnect 3.

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
install Linux*/libjs.{a,so} $RPM_BUILD_ROOT%{_libdir}
install Linux*/jsautocfg.h $RPM_BUILD_ROOT%{_includedir}/js
install js.msg jsapi.h jsarray.h jsarena.h jsatom.h jsbit.h jsbool.h \
	jsclist.h jscntxt.h jscompat.h jsconfig.h jsdate.h jsdbgapi.h \
	jsdhash.h jsemit.h jsfun.h jsgc.h jshash.h jsinterp.h jslock.h \
	jslong.h jsmath.h jsnum.h jsobj.h jsopcode.tbl jsopcode.h jsosdep.h \
	jsotypes.h jsparse.h jsprf.h jsprvtd.h jspubtd.h jsregexp.h jsscan.h \
	jsscope.h jsscript.h jsstr.h jstypes.h jsutil.h jsxdrapi.h jsstddef.h \
	$RPM_BUILD_ROOT%{_includedir}/js

%if 0%{?_with_java:1}
install liveconnect/Linux*/libjsj.{a,so} $RPM_BUILD_ROOT%{_libdir}
install liveconnect/Linux*/lcshell $RPM_BUILD_ROOT%{_bindir}
install liveconnect/classes/Linux*/*.jar $RPM_BUILD_ROOT%{classdir}
install liveconnect/{jsjava.h,nsI*.h,_jni/*.h} $RPM_BUILD_ROOT%{_includedir}/js
%endif

%{__make} -C perlconnect install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f perlconnect/README.html README-perlconnect.html

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
%attr(755,root,root) %{_libdir}/libjs.so

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/js
%{_includedir}/js/js.msg
%{_includedir}/js/jsopcode.tbl
%{_includedir}/js/js[!j]*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libjs.a

%if 0%{?_with_java:1}
%files java
%defattr(644,root,root,755)
%doc src/liveconnect/README.html
%attr(755,root,root) %{_bindir}/lcshell
%attr(755,root,root) %{_libdir}/libjsj.so
%{classdir}/*.jar

%files java-devel
%defattr(644,root,root,755)
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
