%bcond_without javadoc

%bcond_with tests

%define java_home %{_jvmdir}/jre-17-openjdk

Name:          jss
Summary:       Java Security Services
URL:           http://www.dogtagpki.org/wiki/JSS
License:       MPLv1.1 or GPLv2+ or LGPLv2+
Version:       5.4.0
Release:       1
Source0:       https://github.com/dogtagpki/jss/archive/v%{version}/%{name}-%{version}.tar.gz 

BuildRequires: make cmake >= 3.14 gcc-c++ nspr-devel >= 4.13.1 nss-devel >= 3.66 nss-tools >= 3.66
BuildRequires: jpackage-utils slf4j glassfish-jaxb-api slf4j-jdk14 apache-commons-codec junit
BuildRequires: zip unzip java-17-openjdk-devel apache-commons-lang3

Requires:      nss >= 3.66  jpackage-utils slf4j slf4j-jdk14 java-17-openjdk-headless apache-commons-lang3

Conflicts:     ldapjdk < 4.20 idm-console-framework < 1.2 tomcatjss < 7.6.0 pki-base < 10.10.0

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

export JAVA_HOME=%{java_home}

export BUILD_OPT=1

CFLAGS="-g $RPM_OPT_FLAGS"
export CFLAGS

modutil -dbdir /etc/pki/nssdb -chkfips true | grep -q enabled && export FIPS_ENABLED=1

./build.sh \
    %{?_verbose:-v} \
    --work-dir=%{_vpath_builddir} \
    --prefix-dir=%{_prefix} \
    --include-dir=%{_includedir} \
    --lib-dir=%{_libdir} \
    --sysconf-dir=%{_sysconfdir} \
    --share-dir=%{_datadir} \
    --cmake=%{__cmake} \
    --java-home=%{java_home} \
    --jni-dir=%{_jnidir} \
    --version=%{version} \
    %{!?with_javadoc:--without-javadoc} \
    %{?with_tests:--with-tests} \
    dist

%install
./build.sh \
    %{?_verbose:-v} \
    --work-dir=%{_vpath_builddir} \
    --install-dir=%{buildroot} \
    install

%files
%defattr(-,root,root,-)
%doc jss.html 
%license MPL-1.1.txt gpl.txt lgpl.txt symkey/LICENSE
%{_libdir}/*
%{_jnidir}/*

%files help
%defattr(-,root,root,-)
%{_javadocdir}/jss/

%changelog
* Wed Apr 26 2023 xu_ping <707078654@qq.com> - 5.4.0-1
- Upgrade to 5.4.0

* Thu Feb 23 2023 lilong <lilong@kylinos.cn> - 5.3.0-1
- Upgrade to 5.3.0

* Mon Jun 06 2022 Ge Wang <wangge20@h-partners.com> - 5.1.0-1
- Upgrade version to 5.1.0

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 4.6.2-5
- DESC: delete -S git from %autosetup, and delete BuildRequires git

* Wed Aug 05 2020 lingsheng <lingsheng@huawei.com> - 4.6.2-4
- Fix build with nss 3.54

* Thu Apr 16 2020 lizhenhua <lizhenhua21@huawei.com> - 4.6.2-3
- Package init
