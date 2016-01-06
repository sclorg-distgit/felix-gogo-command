%global project felix
%global bundle org.apache.felix.gogo.command
%global groupId org.apache.felix
%global artifactId %{bundle}

%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package %{project}-gogo-command}
%{?java_common_find_provides_and_requires}

Name:           %{?scl_prefix}%{project}-gogo-command
Version:        0.12.0
Release:        12%{?dist}
Summary:        Apache Felix Gogo Command

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://felix.apache.org
Source0:        http://www.apache.org/dist/felix/%{bundle}-%{version}-project.tar.gz

Patch0:         felix-gogo-command-pom.xml.patch
Patch1:         java7compatibility.patch

BuildArch:      noarch

# This is to ensure we get OpenJDK and not GCJ
BuildRequires:  java-1.7.0-openjdk-devel >= 1:1.7.0
BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix_maven}maven-dependency-plugin

BuildRequires:  %{?scl_prefix}felix-gogo-runtime
BuildRequires:  %{?scl_prefix}felix-gogo-parent

%description
Provides basic shell commands for Gogo.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%setup -q -n %{bundle}-%{version} 
%patch0 -p1
%patch1 -p1

%build
scl enable %{scl_maven} %{scl} - <<"EOF"
%pom_xpath_inject "pom:dependencies/pom:dependency[pom:artifactId[text()='org.osgi.compendium']]" "<scope>provided</scope>"
%pom_xpath_inject "pom:dependencies/pom:dependency[pom:artifactId[text()='org.apache.felix.bundlerepository']]" "<scope>provided</scope>"
%mvn_build
EOF

%install
scl enable %{scl_maven} %{scl} - <<"EOF"
%mvn_install
EOF

%files -f .mfiles
%dir %{_javadir}/felix-gogo-command
%dir %{_mavenpomdir}/felix-gogo-command
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Fri Jan 16 2015 Mat Booth <mat.booth@redhat.com> - 0.12.0-12
- Fix unowned directories

* Fri Jan 16 2015 Mat Booth <mat.booth@redhat.com> - 0.12.0-11
- Related: rhbz#1175105 - Rebuilt to regenerate requires/provides

* Wed May 21 2014 Mat Booth <mat.booth@redhat.com> - 0.12.0-10
- Removed R's that are only needed when running on a felix osgi runtime

* Sat May 17 2014 Sami Wagiaalla <swagiaal@redhat.com> 0.12.0-9
- Use pkg_name instead of name for javadoc location.

* Sat May 17 2014 Sami Wagiaalla <swagiaal@redhat.com> 0.12.0-8
- Build for DTS 3 build
- Install javadoc manually
- Use java-1.7.0-openjdk-devel for java-devel req.

* Fri May 16 2014 Sami Wagiaalla <swagiaal@redhat.com> 0.12.0-8
- Prepare for DTS 3 build
- Copy mvn_rpmbuild fix from rawhide.
- Use maven scl for maven packages.
- enable maven scl for maven commands.

* Wed Feb 13 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-7
- Make the package noarch.

* Fri Dec 7 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-6
- Remove unnecessary runtime dependencies.

* Wed Nov 21 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-5
- Added Exclusive arch.

* Fri Nov 9 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.12.0-1
- Initial contribution to SCL.
