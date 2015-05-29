# remirepo/fedora spec file for php-phpunit-PHPUnit-MockObject
#
# Copyright (c) 2013-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    253c005852591fd547fc18cd5b7b43a1ec82d8f7
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   phpunit-mock-objects
%global php_home     %{_datadir}/php
%global pear_name    PHPUnit_MockObject
%global pear_channel pear.phpunit.de
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-phpunit-PHPUnit-MockObject
Version:        2.3.3
Release:        1%{?dist}
Summary:        Mock Object library for PHPUnit

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Autoload template
Source1:        Autoload.php.in

# Temporary workaround, under investigation
Patch0:         %{gh_project}-rpm.patch

# Upstream patches

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.4"
BuildRequires:  php-pear-PHPUnit >= 4.4.0
%endif

# From composer.json, "require": {
#        "php": ">=5.3.3",
#        "phpunit/php-text-template": "~1.2",
#        "doctrine/instantiator": "~1.0,>=1.0.2",
Requires:       php(language) >= 5.3.3
Requires:       php-composer(phpunit/php-text-template) >= 1.2
Requires:       php-composer(phpunit/php-text-template) <  2
Requires:       php-composer(doctrine/instantiator) >= 1.0.2
Requires:       php-composer(doctrine/instantiator) <  2
# From composer.json, "suggest": {
#        "ext-soap": "*"
Requires:       php-soap
# From phpcompatinfo report for version 2.3.1
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl

Provides:       php-composer(phpunit/phpunit-mock-objects) = %{version}


%description
Mock Object library for PHPUnit


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1

find . -name \*.orig -exec rm {} \; -print


%build
phpab \
  --output   src/Framework/MockObject/Autoload.php \
  --template %{SOURCE1} \
  src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/PHPUnit


%if %{with_tests}
%check
# No phpcov
grep -v 'log' phpunit.xml.dist > phpunit.xml

# Generate autoloader for tests
phpab --output tests/_fixture/autoload.php tests/_fixture/

# Fix bootstrap
mkdir vendor
ln -s ../src/Framework/MockObject/Autoload.php vendor/autoload.php
cat <<EOF >>tests/bootstrap.php
require __DIR__ . '/_fixture/autoload.php';
EOF

# Run tests
phpunit
%endif


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CONTRIBUTING.md README.md composer.json
%dir %{php_home}/PHPUnit
%dir %{php_home}/PHPUnit/Framework
     %{php_home}/PHPUnit/Framework/MockObject


%changelog
* Fri May 29 2015 Remi Collet <remi@fedoraproject.org> - 2.3.3-1
- update to 2.3.3

* Thu May 28 2015 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- update to 2.3.2

* Thu Apr  2 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- update to 2.3.1

* Fri Oct  3 2014 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- update to 2.3.0 for PHPUnit 4.3.0
- drop dependency on ocramius/instantiator
- add depencency on doctrine/instantiator

* Fri Oct  3 2014 Remi Collet <remi@fedoraproject.org> - 2.3.0-0
- bootstrap build

* Sun Sep  7 2014 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- update to 2.2.1
- enable test suite

* Mon Aug 11 2014 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0
- add dependency on ocramius/instantiator
- fix license handling

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 2.1.5-1
- update to 2.1.5

* Thu Jun 12 2014 Remi Collet <remi@fedoraproject.org> - 2.1.4-1
- update to 2.1.4
- add upstream patch to fix unserialize issue
  https://github.com/sebastianbergmann/phpunit-mock-objects/pull/176

* Sat Jun  7 2014 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- update to 2.1.3

* Sat Jun  7 2014 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- update to 2.1.2

* Fri Jun  6 2014 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- update to 2.1.1

* Fri May 30 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-3
- upstream fix for php 5.4.29 and 5.5.13

* Tue May  6 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- workaround to autoload issue during check

* Sat May  3 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0 for PHPUnit 4.1

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-2
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- update to 2.0.5
- sources from gthub
- run tests when build --with tests option

* Sun Jan 13 2013 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Version 1.2.3 (stable) - API 1.2.0 (stable)

* Mon Nov  5 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Version 1.2.2 (stable) - API 1.2.0 (stable)

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Version 1.2.1 (stable) - API 1.2.0 (stable)

* Thu Sep 20 2012 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Version 1.2.0 (stable) - API 1.2.0 (stable)
- raise dependencies: php 5.3.3, PHPUnit 3.7.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Version 1.1.1 (stable) - API 1.1.0 (stable)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)

* Fri Jun 10 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.9-1
- Version 1.0.9 (stable) - API 1.0.4 (stable)
- remove PEAR hack (only needed for EPEL)
- raise PEAR dependency to 1.9.2

* Tue May  3 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.8-2
- rebuild for doc in /usr/share/doc/pear

* Wed Feb 16 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.8-1
- Version 1.0.8 (stable) - API 1.0.4 (stable)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 05 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.7-1
- Version 1.0.7 (stable) - API 1.0.4 (stable)

* Tue Jan 18 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.6-1
- Version 1.0.6 (stable) - API 1.0.4 (stable)

* Tue Jan 18 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.5-1
- Version 1.0.5 (stable) - API 1.0.4 (stable)
- CHANGELOG and LICENSE are now in the tarball

* Mon Nov 22 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.3-1
- Version 1.0.3 (stable) - API 1.0.3 (stable)

* Wed Nov 17 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.2-1
- Version 1.0.2 (stable) - API 1.0.0 (stable)

* Fri Nov 05 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.1-2
- lower PEAR dependency to allow el6 build
- fix URL

* Mon Oct 25 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.0 (stable)

* Sun Sep 26 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-1
- initial generated spec + clean

