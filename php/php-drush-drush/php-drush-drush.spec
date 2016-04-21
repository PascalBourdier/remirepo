# Awaiting the following issue fixes from upstream:
# * PEAR license file (http://drupal.org/node/1643680)
# * PEAR role="doc" (http://drupal.org/node/1643660)
# * PEAR role="test" (http://drupal.org/node/1643676)
# * PEAR extra files (http://drupal.org/node/1772518)
# * drush.bat (http://drupal.org/node/1704986)

%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}

%global pear_channel pear.drush.org
%global pear_name    drush

# PEAR version adds an extra digit
%global pear_version %{version}.0

# Tests are only run with rpmbuild "--with tests"
# Tests require download access and a running MariaDB/MySQL server with root
#     user and no password
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:             php-drush-%{pear_name}
Version:          6.2.0
Release:          6%{?dist}
Summary:          Command line shell and Unix scripting interface for Drupal

Group:            Development/Libraries
License:          GPLv2+
URL:              http://www.drush.org
Source0:          http://%{pear_channel}/get/%{pear_name}-%{pear_version}.tgz

Provides:         php-pear(%{pear_channel}/%{pear_name}) = %{version}
Obsoletes:        drupal6-drush < %{version}-%{release}
Provides:         drupal6-drush = %{version}-%{release}
Obsoletes:        drupal7-drush < %{version}-%{release}
Provides:         drupal7-drush = %{version}-%{release}

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
BuildRequires:    php-pear(PEAR)
BuildRequires:    php-channel(%{pear_channel})
#BuildRequires:    help2man
%if %{with_tests}
BuildRequires:    php-pear(pear.phpunit.de/PHPUnit) >= 3.5
BuildRequires:    php-pear(Console_Table)
%endif

Requires:         php(language) >= 5.3.0
Requires:         php-pear(PEAR)
Requires:         php-channel(%{pear_channel})
Requires:         php-pear(Console_Table)
Requires:         php-symfony-yaml
Requires:         git >= 1.7
Requires(post):   %{__pear}
Requires(postun): %{__pear}
# phpci requires
Requires:         php-ctype
Requires:         php-date
Requires:         php-dom
Requires:         php-fileinfo
Requires:         php-filter
Requires:         php-hash
Requires:         php-iconv
Requires:         php-json
Requires:         php-mbstring
Requires:         php-pcre
Requires:         php-pdo
Requires:         php-posix
Requires:         php-reflection
Requires:         php-simplexml
Requires:         php-spl
Requires:         patch

%description
Drush is a command line shell and Unix scripting interface for Drupal.  If
you are unfamiliar with shell scripting, reviewing the documentation for your
shell (e.g. man bash) or reading an online tutorial (e.g. search for "bash
tutorial") will help you get the most out of Drush.

Drush core ships with lots of useful commands for interacting with code like
modules/themes/profiles. Similarly, it runs update.php, executes sql queries
and DB migrations, and misc utilities like run cron or clear cache.

Works with Drupal 6, Drupal 7, and usually Drupal 8.

NOTE: You must manually install your required database driver
      (ex: php-mysql, php-mysqli, php-pgsql)


%prep
%setup -q -c

# Remove .travis.yml and .gitignore files from package.xml
# *** Upstream issue: http://drupal.org/node/1772518
sed -e '/.travis.yml/d' \
    -e '/.gitignore/d' \
    -i package.xml

# Remove bundled Symfony YAML
# *** Upstream issue: ...
sed '/name="lib\/Yaml/d' \
    -i package.xml
# Update location and remove PEAR checksum
sed -e "s#\$path\s*=\s*.*#\$path = '%{pear_phpdir}/Symfony/Component/Yaml';#" \
    -e '/DRUSH_YAML_VERSION/d' \
    -i %{pear_name}-%{pear_version}/commands/core/outputformat/yaml.inc
sed '/commands\/core\/outputformat\/yaml.inc/s/md5sum="[^"]*"\s*//' \
    -i package.xml

# Update package.xml for files identified with role="php"
# instead of role="test":
# - tests/
# *** Upstream issue: http://drupal.org/node/1643676
sed '/name="tests\//s/role="php"/role="test"/' \
    -i package.xml

# Update package.xml for files identified with role="php"
# instead of role="doc":
# - *.md
# - *.txt
# - composer.json
# - docs/
# - examples/
# *** Upstream issue: http://drupal.org/node/1643660
sed -e '/name="[^"]*\.md"/s/role="[^"]*"/role="doc"/' \
    -e '/name="[^"]*\.txt"/s/role="[^"]*"/role="doc"/' \
    -e '/name="composer.json/s/role="php"/role="doc"/' \
    -e '/name="docs\//s/role="php"/role="doc"/' \
    -e '/name="examples\//s/role="php"/role="doc"/' \
    -i package.xml

# Remove drush.bat
# *** Upstream issue: http://drupal.org/node/1704986
sed -e '/<file.*name="drush.bat"/,/<\/file>/d' \
    -e '/<install.*drush.bat/d' \
    -i package.xml

# Fix rpmlint "W: wrong-file-end-of-line-encoding
# /usr/share/doc/pear/drush/examples/sandwich.txt"
sed 's/\r//' -i %{pear_name}-%{pear_version}/examples/sandwich.txt
sed '/examples\/sandwich.txt/s/md5sum="[^"]*"//' -i package.xml

# Use "which php" instead of "which php-cli"
sed 's/which php-cli/which php/' -i %{pear_name}-%{pear_version}/drush
sed '/name="drush"/s/md5sum=".*" name/name/' -i package.xml

# package.xml is version 2.0
mv package.xml %{pear_name}-%{pear_version}/%{name}.xml


%build
# Build man page
#cd %%{pear_name}-%%{pear_version}
#sed -e 's#@pear_directory@/drush#`dirname -- "$0"`#' \
#    -e 's#@php_bin@#%%{_bindir}/php#' \
#    drush > drush-help2man
#chmod +x drush-help2man
#help2man --no-info ./drush-help2man > drush.1
#sed -e 's/drush-help2man/drush/g' \
#    -e 's/DRUSH-HELP2MAN/DRUSH/g' \
#    -i drush.1

%install
cd %{pear_name}-%{pear_version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Fix some file permissions
#chmod a+x %%{buildroot}%%{pear_phpdir}/%%{pear_name}/drush.php
#chmod a+x %%{buildroot}%%{pear_phpdir}/%%{pear_name}/drush.complete.sh
#chmod a+x %%{buildroot}%%{pear_testdir}/%%{pear_name}/tests/runner.php

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

# Install man page
#mkdir -p %%{buildroot}%%{_mandir}/man1
#cp -p drush.1 %%{buildroot}%%{_mandir}/man1/

# Create lib directory
mkdir -pm 0755 %{buildroot}%{pear_phpdir}/%{pear_name}/lib


%check
%if %{with_tests}
    cd %{pear_name}-%{version}/tests
    %{_bindir}/phpunit .
%else
: Tests skipped, missing '--with tests' option
%endif


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
#%doc %%{_mandir}/man1/drush.1*
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/%{pear_name}
%{pear_testdir}/%{pear_name}
%{_bindir}/drush*


%changelog
* Tue Apr 19 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 6.2.0-6
- Update bin to search for "php" rather than "php-cli"
- No "help2man" BuildRequires since man page creation is disabled

* Thu Dec 12 2013 Remi Collet <remi@fedoraproject.org> 6.2.0-1
- backport 6.2.0 for remi repo.

* Mon Dec 09 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 6.2.0-1
- Updated to 6.2.0 (BZ 997843, 1016260)
- Fixed drush bin as regualr user (BZ 1013501)
- PHP minimum version 5.2 => 5.3.0
- Added the following requires: php-symfony-yaml, php-filter, php-mbstring
- Removed the following requires: php-mysql, php-mysqli, php-pgsql
- Removed man page (for now) as it was causing koji build errors

* Wed May  8 2013 Remi Collet <remi@fedoraproject.org> 5.9.0-1
- backport 5.9.0 for remi repo.

* Wed May 08 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 5.9.0-1
- Updated to version 5.9.0

* Thu Apr  4 2013 Remi Collet <remi@fedoraproject.org> 5.8.0-4
- backport rawhide changes for remi repo.

* Wed Apr 03 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 5.8.0-4
- Added obsolete and virtual provide of drupal7-drush

* Wed Apr 03 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 5.8.0-3
- Added php-pear(Console_Table) build require

* Wed Mar 20 2013 Remi Collet <remi@fedoraproject.org> 5.8.0-2
- backport 5.8.0 for remi repo.

* Sun Mar 17 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 5.8.0-2
- Removed drush.bat
- Fixed rpmlint wrong-file-end-of-line-encoding warning
- Added man page

* Tue Nov 27 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 5.8.0-1
- Updated to upstream version 5.8.0

* Thu Nov  8 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 5.7.0-1
- Initial package
