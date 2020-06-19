Name:          jss
Summary:       Java Security Services
URL:           http://www.dogtagpki.org/wiki/JSS
License:       MPLv1.1 or GPLv2+ or LGPLv2+
Version:       4.6.2
Release:       3
Source:        https://github.com/dogtagpki/jss/archive/v%{version}/jss-%{version}.tar.gz
Patch0001:     0001-Fix-NativeProxy-reference-tracker.patch

BuildRequires: git make cmake gcc-c++ nspr-devel >= 4.13.1 nss-devel >= 3.30 nss-tools >= 3.30 java-devel
BuildRequires: jpackage-utils slf4j glassfish-jaxb-api slf4j-jdk14 apache-commons-lang apache-commons-codec
BuildRequires: junit

Requires:      nss >= 3.30 java-headless jpackage-utils slf4j glassfish-jaxb-api
Requires:      slf4j-jdk14 apache-commons-lang apache-commons-codec

Conflicts:     ldapjdk < 4.20 idm-console-framework < 1.2 tomcatjss < 7.3.4 pki-base < 10.6.5

%description
JSS offers a implementation for java-based applications to use native NSS.

%package       help
Summary:       JSS Javadocs
Requires:      jss = %{version}-%{release}
Provides:      jss-javadoc = %{version}-%{release}
Obsoletes:     jss-javadoc < %{version}-%{release}
%description   help
API documentation for JSS.

%prep
%autosetup -n jss-%{version} -p 1 -S git

%build

%set_build_flags

[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java

export BUILD_OPT=1

export CFLAGS="-g $RPM_OPT_FLAGS"

modutil -dbdir /etc/pki/nssdb -chkfips true | grep -q enabled && export FIPS_ENABLED=1

rm -rf build && install -d build && cd build
%cmake -DJAVA_HOME=%{java_home} -DJAVA_LIB_INSTALL_DIR=%{_jnidir} ..

%make_build all
%make_build javadoc || true

%install
mkdir -p $RPM_BUILD_ROOT%{_jnidir}
chmod 755 $RPM_BUILD_ROOT%{_jnidir}
cp build/jss4.jar ${RPM_BUILD_ROOT}%{_jnidir}
chmod 644 ${RPM_BUILD_ROOT}%{_jnidir}/jss4.jar

mkdir -p $RPM_BUILD_ROOT%{_libdir}/jss
chmod 755 $RPM_BUILD_ROOT%{_libdir}/jss
cp build/libjss4.so ${RPM_BUILD_ROOT}%{_libdir}/jss
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/jss/libjss4.so

pushd  ${RPM_BUILD_ROOT}%{_libdir}/jss
ln -fs %{_jnidir}/jss4.jar jss4.jar
popd

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/jss-%{version}
chmod 755 $RPM_BUILD_ROOT%{_javadocdir}/jss-%{version}
cp -rp build/docs/* jss.html *.txt $RPM_BUILD_ROOT%{_javadocdir}/jss-%{version}

%files
%defattr(-,root,root,-)
%doc jss.html MPL-1.1.txt gpl.txt lgpl.txt
%{_libdir}/*
%{_jnidir}/*

%files help
%defattr(-,root,root,-)
%{_javadocdir}/jss-%{version}/

%changelog
* Thu Apr 16 2020 lizhenhua <lizhenhua21@huawei.com> - 4.6.2-3
- Package init
