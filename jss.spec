Name:          jss
Summary:       Java Security Services
URL:           http://www.dogtagpki.org/wiki/JSS
License:       MPLv1.1 or GPLv2+ or LGPLv2+
Version:       5.1.0
Release:       1
Source:        https://github.com/dogtagpki/jss/archive/refs/tags/jss-%{version}.tar.gz

BuildRequires: make cmake gcc-c++ nspr-devel >= 4.13.1 nss-devel >= 3.30 nss-tools >= 3.30 java-devel
BuildRequires: jpackage-utils slf4j glassfish-jaxb-api slf4j-jdk14 apache-commons-lang apache-commons-codec
BuildRequires: junit

BuildRequires: zip unzip java-11-openjdk-devel apache-commons-lang3

Requires:      nss >= 3.30 java-headless jpackage-utils slf4j glassfish-jaxb-api
Requires:      slf4j-jdk14 apache-commons-lang apache-commons-codec

Requires: java-11-openjdk-headless apache-commons-lang3

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
%autosetup -n jss-%{version} -p 1

%build

%set_build_flags
home_path=`ls /usr/lib/jvm | grep java-11-openjdk`
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/${home_path}

export BUILD_OPT=1

export CFLAGS="-g $RPM_OPT_FLAGS"

modutil -dbdir /etc/pki/nssdb -chkfips true | grep -q enabled && export FIPS_ENABLED=1


./build.sh \
    %{?_verbose:-v} \
    --work-dir=build \
    --jni-dir=%{_jnidir} \
    --lib-dir=%{_libdir} \
    --version=%{version} \
    dist

%install
mkdir -p $RPM_BUILD_ROOT%{_jnidir}
chmod 755 $RPM_BUILD_ROOT%{_jnidir}
cp build/jss.jar ${RPM_BUILD_ROOT}%{_jnidir}
chmod 644 ${RPM_BUILD_ROOT}%{_jnidir}/jss.jar

mkdir -p $RPM_BUILD_ROOT%{_libdir}/jss
chmod 755 $RPM_BUILD_ROOT%{_libdir}/jss
cp build/libjss.so ${RPM_BUILD_ROOT}%{_libdir}/jss
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/jss/libjss.so

pushd  ${RPM_BUILD_ROOT}%{_libdir}/jss
ln -fs %{_jnidir}/jss.jar jss.jar
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
* Mon Jun 06 2022 Ge Wang <wangge20@h-partners.com> - 5.1.0-1
- Upgrade version to 5.1.0

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 4.6.2-5
- DESC: delete -S git from %autosetup, and delete BuildRequires git

* Wed Aug 05 2020 lingsheng <lingsheng@huawei.com> - 4.6.2-4
- Fix build with nss 3.54

* Thu Apr 16 2020 lizhenhua <lizhenhua21@huawei.com> - 4.6.2-3
- Package init
