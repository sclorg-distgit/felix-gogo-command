%{?scl:%scl_package felix-gogo-command}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 1

Name:           %{?scl_prefix}felix-gogo-command
Version:        0.16.0
Release:        3.%{baserelease}%{?dist}
Summary:        Apache Felix Gogo Command

License:        ASL 2.0
URL:            http://felix.apache.org
Source0:        http://www.apache.org/dist/felix/org.apache.felix.gogo.command-%{version}-project.tar.gz

Patch0:         felix-gogo-command-pom.xml.patch

BuildArch:      noarch

BuildRequires:  %{?scl_prefix_maven}maven-local
BuildRequires:  %{?scl_prefix}mvn(org.apache.felix:gogo-parent:pom:)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.felix:org.apache.felix.bundlerepository)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.apache.felix:org.apache.felix.framework)
BuildRequires:  %{?scl_prefix}mvn(org.apache.felix:org.apache.felix.gogo.runtime)
BuildRequires:  %{?scl_prefix_maven}mvn(org.osgi:org.osgi.compendium)
BuildRequires:  %{?scl_prefix}mvn(org.mockito:mockito-all)

%description
Provides basic shell commands for Gogo.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n org.apache.felix.gogo.command-%{version}
%patch0 -p1

# These deps are provided at runtime by the osgi framework in which are running
# Adding "provided" scope here avoids unnecessary deps on the felix stack if we
# are running in a different osgi container like equinox, for example
%pom_xpath_inject "pom:dependencies/pom:dependency[pom:artifactId[text()='org.apache.felix.framework']]" "<scope>provided</scope>"
%pom_xpath_inject "pom:dependencies/pom:dependency[pom:artifactId[text()='org.osgi.compendium']]" "<scope>provided</scope>"
%pom_xpath_inject "pom:dependencies/pom:dependency[pom:artifactId[text()='org.apache.felix.bundlerepository']]" "<scope>provided</scope>"

# Upstream distribution does not have this requirement, we don't need it here either
sed -i -e 's|\*</Import-Package>|!org.apache.felix.bundlerepository,*</Import-Package>|' pom.xml
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_build
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Thu Jul 21 2016 Mat Booth <mat.booth@redhat.com> - 0.16.0-3.1
- Auto SCL-ise package for rh-eclipse46 collection

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 07 2015 Mat Booth <mat.booth@redhat.com> - 0.16.0-2
- Remove unneeded hard dep on felix-bundlerepository

* Tue Oct 6 2015 Alexander Kurtakov <akurtako@redhat.com> 0.16.0-1
- Update to upstream 0.16.0 release.
- Drop no longer needed Java 7 compatibility patch.

* Mon Jun 29 2015 Mat Booth <mat.booth@redhat.com> - 0.14.0-5
- Drop incomplete and forbidden SCL macros

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 30 2015 Mat Booth <mat.booth@redhat.com> - 0.14.0-3
- Avoid unnecessary runtime deps and re-generate build-deps

* Thu Jul 03 2014 Mat Booth <mat.booth@redhat.com> - 0.14.0-2
- BR/R: gogo-runtime >= 0.12.0

* Thu Jul 3 2014 Alexander Kurtakov <akurtako@redhat.com> 0.14.0-1
- Update to 0.14.0.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Alexander Kurtakov <akurtako@redhat.com> 0.12.0-10
- Start using mvn_build/install.

* Mon Aug 5 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-9
- Fix FTBS.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-7
- Initial SCLization.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.12.0-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-3
- Dependency to Java 7 added.
- Sources are patched to compile with OpenJDK 7.

* Tue Jan 10 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-2
- description formatting removed
- jar_repack removed
- license added to the javadoc

* Tue Jan 10 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-1
- Release 0.12.0