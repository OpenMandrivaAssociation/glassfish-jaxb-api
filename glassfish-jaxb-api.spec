%_javapackages_macros
%global oname jaxb-api
Name:          glassfish-jaxb-api
Version:       2.2.9
Release:       4.0%{?dist}
Summary:       Java Architecture for XML Binding
License:       CDDL or GPLv2 with exception
URL:           http://jaxb.java.net/
# jaxb api and impl have different version
# svn export https://svn.java.net/svn/jaxb~version2/tags/jaxb-2_2_6/tools/lib/redist/jaxb-api-src.zip

Source0:       http://repo1.maven.org/maven2/javax/xml/bind/%{oname}/%{version}/%{oname}-%{version}-sources.jar
Source1:       http://repo1.maven.org/maven2/javax/xml/bind/%{oname}/%{version}/%{oname}-%{version}.pom

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: java-javadoc
BuildRequires: jvnet-parent

BuildRequires: maven-local
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-resources-plugin
BuildRequires: maven-shared-osgi
Requires:      java >= 1:1.6.0
Requires:      jvnet-parent
BuildArch:     noarch

# The Fedora Packaging Committee granted openjdk a bundling exception to carry JAXP and
# JAX-WS (glassfish doesn't need one, since it is the upstream for these files).
# Reference: https://fedorahosted.org/fpc/ticket/292

%description
Glassfish - JAXB (JSR 222) API.

%package javadoc
Summary:       Javadoc for %{oname}
Requires:      %{name} = %{version}-%{release} 

%description javadoc
Glassfish - JAXB (JSR 222) API.

This package contains javadoc for %{name}.

%prep
%setup -T -q -c

# fixing incomplete source directory structure
mkdir -p src/main/java

(
  cd src/main/java
  unzip -qq %{SOURCE0}
  rm -rf META-INF
)

cp -p %{SOURCE1} pom.xml

sed -i 's|<location>${basedir}/offline-javadoc</location>|<location>%{_javadocdir}/java</location>|' pom.xml

%build

%mvn_file :%{oname} %{oname}
%mvn_build

%install
%mvn_install

mv %{buildroot}%{_javadocdir}/%{name} \
 %{buildroot}%{_javadocdir}/%{oname}

%files -f .mfiles

%files javadoc
%{_javadocdir}/%{oname}
