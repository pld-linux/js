#
# Conditional build:
%bcond_without	threads	# thread-safe library (requires nspr)
%bcond_without	java	# libjsj and lshell
#
Summary:	JavaScript Reference Implementation
Summary(pl.UTF-8):	Wzorcowa implementacja JavaScriptu
Name:		js
Version:	1.7.0
Release:	12
Epoch:		2
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		Development/Languages
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/%{name}-%{version}.tar.gz
# Source0-md5:	5571134c3863686b623ebe4e6b1f6fe6
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-java.patch
Patch2:		%{name}-build.patch
URL:		http://www.mozilla.org/js/
%{?with_java:BuildRequires:	jdk}
%{?with_java:BuildRequires:	jpackage-utils}
%{?with_threads:BuildRequires:	nspr-devel}
BuildRequires:	perl-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.294
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
# dead, removed upstream
Obsoletes:	perl-JS
Conflicts:	njs
%{?with_threads:Provides:	js(threads)}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		classdir	%{_datadir}/java

%description
JavaScript Reference Implementation (codename SpiderMonkey). The
package contains JavaScript runtime (compiler, interpreter,
decompiler, garbage collector, atom manager, standard classes) and
small "shell" program that can be used interactively and with .js
files to run scripts.

%description -l pl.UTF-8
Wzorcowa implementacja JavaScriptu (o nazwie kodowej SpiderMonkey).
Pakiet zawiera środowisko uruchomieniowe (kompilator, interpreter,
dekompilator, odśmiecacz, standardowe klasy) i niewielką powłokę,
która może być używana interaktywnie lub z plikami .js do uruchamiania
skryptów.

%package libs
Summary:	JavaScript Reference Implementation library
Summary(pl.UTF-8):	Biblioteka wzorcowej implementacja JavaScriptu
Group:		Libraries
Conflicts:	js < 1.7.0-8

%description libs
JavaScript Reference Implementation (codename SpiderMonkey) library.

%description libs -l pl.UTF-8
Biblioteka wzorcowej implementacja JavaScriptu (SpiderMonkey).

%package devel
Summary:	Header files for JavaScript reference library
Summary(pl.UTF-8):	Pliki nagłówkowe do biblioteki JavaScript
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Conflicts:	njs-devel
%{?with_threads:Provides:	js-devel(threads)}

%description devel
Header files for JavaScript reference library.

%description devel -l pl.UTF-8
Pliki nagłówkowe do biblioteki JavaScript.

%package static
Summary:	Static JavaScript reference library
Summary(pl.UTF-8):	Statyczna biblioteka JavaScript
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Conflicts:	njs-static
%{?with_threads:Provides:	js-static(threads)}

%description static
Static version of JavaScript reference library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki JavaScript.

%package java
Summary:	JavaScript LiveConnect Version 3 implementation
Summary(pl.UTF-8):	Implementacja JavaScript LiveConnect w wersji 3
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

%description java -l pl.UTF-8
LiveConnect to biblioteka pozwalająca na współpracę maszyn wirtualnych
JavaScriptu i Javy. W szczególności pozwala z poziomu JavaScriptu na
dostęp do pól Javy, wywoływanie metod Javy oraz z poziomu Javy na
dostęp do składowych obiektów JavaScriptu i wykonywanie dowolnego kodu
w JavaScripcie. LiveConnect oryginalnie był zintegrowaną częścią
przeglądarki Netscape Navigator oraz Netscape JavaScript działającego
po stronie serwera. Teraz jest to samodzielna biblioteka, którą można
osadzać w innych projektach, takich jak przeglądarka Mozilla.

%package java-devel
Summary:	JavaScript LiveConnect 3 implementation header files
Summary(pl.UTF-8):	Pliki nagłówkowe implementacji JavaScript LiveConnect 3
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Requires:	%{name}-java = %{epoch}:%{version}-%{release}

%description java-devel
JavaScript LiveConnect 3 implementation header files.

%description java-devel -l pl.UTF-8
Pliki nagłówkowe implementacji JavaScript LiveConnect 3.

%package java-static
Summary:	JavaScript Live Connect 3 implementation static library
Summary(pl.UTF-8):	Biblioteka statyczna implementacji JavaScript LiveConnect 3
Group:		Development/Libraries
Requires:	%{name}-java-devel = %{epoch}:%{version}-%{release}

%description java-static
JavaScript Live Connect 3 implementation static library.

%description java-static -l pl.UTF-8
Biblioteka statyczna implementacji JavaScript LiveConnect 3.

%prep
%setup -q -n %{name}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

echo 'SONAME=libjs.so.1' >> src/Makefile.ref
echo 'SONAME=libjsj.so.1' >> src/liveconnect/Makefile.ref

%ifarch %{x8664}
sed -i -e 's#i386#amd64#g' src/liveconnect/Makefile.ref src/liveconnect/config/*.mk
sed -i -e 's#lib/amd64/client#lib/amd64/server#g' src/liveconnect/Makefile.ref src/liveconnect/config/*.mk
%endif

%build
%{__make} -j1 -C src -f Makefile.ref \
	%{!?debug:BUILD_OPT=1} \
	OPTIMIZER="%{rpmcflags} -DHAVE_VA_COPY -DVA_COPY=va_copy -DJS_C_STRINGS_ARE_UTF8=1" \
	JS_READLINE=1 \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	MKSHLIB="%{__cc} -shared -Wl,-soname=\$(SONAME)" \
	%{?with_threads:JS_THREADSAFE=1} \
	%{?with_java:JS_LIVECONNECT=1 JDK=%{java_home}}

# no UNIX makefiles
# %{__make} -C jsd

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}/js,%{classdir}}

cd src
install Linux*/{js,jscpucfg} $RPM_BUILD_ROOT%{_bindir}
install Linux*/libjs.a $RPM_BUILD_ROOT%{_libdir}
install Linux*/libjs.so $RPM_BUILD_ROOT%{_libdir}/libjs.so.1.0.0
ln -sf libjs.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}/libjs.so.1
ln -sf libjs.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}/libjs.so
install Linux*/{jsautocfg.h,jsautokw.h} $RPM_BUILD_ROOT%{_includedir}/js
install js.msg jsapi.h jsarray.h jsarena.h jsatom.h jsbit.h jsbool.h \
	jsclist.h jscntxt.h jscompat.h jsconfig.h jsdate.h jsdbgapi.h \
	jsdhash.h jsemit.h jsfun.h jsgc.h jshash.h jsinterp.h jsiter.h \
	jslock.h jslong.h jsmath.h jsnum.h jsobj.h jsopcode.tbl jsopcode.h \
	jsosdep.h jsotypes.h jsparse.h jsprf.h jsproto.tbl jsprvtd.h jspubtd.h \
	jsregexp.h jsscan.h jsscope.h jsscript.h jsstddef.h jsstr.h jstypes.h \
	jsutil.h jsxdrapi.h jsxml.h \
	$RPM_BUILD_ROOT%{_includedir}/js

%if %{with java}
install liveconnect/Linux*/libjsj.a $RPM_BUILD_ROOT%{_libdir}
install liveconnect/Linux*/libjsj.so $RPM_BUILD_ROOT%{_libdir}/libjsj.so.1.0.0
ln -sf libjsj.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}/libjsj.so.1
ln -sf libjsj.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}/libjsj.so
install liveconnect/Linux*/lcshell $RPM_BUILD_ROOT%{_bindir}
install liveconnect/classes/Linux*/*.jar $RPM_BUILD_ROOT%{classdir}
install liveconnect/{jsjava.h,nsI*.h,_jni/*.h} $RPM_BUILD_ROOT%{_includedir}/js
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	java -p /sbin/ldconfig
%postun	java -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc src/README.html
%attr(755,root,root) %{_bindir}/js

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjs.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jscpucfg
%attr(755,root,root) %{_libdir}/libjs.so
%dir %{_includedir}/js
%{_includedir}/js/js.msg
%{_includedir}/js/jsopcode.tbl
%{_includedir}/js/jsproto.tbl
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
%attr(755,root,root) %ghost %{_libdir}/libjsj.so.1
%{classdir}/js*.jar

%files java-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjsj.so
%{_includedir}/js/jsjava.h
%{_includedir}/js/n*.h

%files java-static
%defattr(644,root,root,755)
%{_libdir}/libjsj.a
%endif
