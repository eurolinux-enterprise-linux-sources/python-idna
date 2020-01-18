%if 0%{?fedora}
%global with_python3 1
%endif

%global srcname idna

Name:           python-%{srcname}
Version:        2.4
Release:        1%{?dist}
Summary:        Internationalized Domain Names in Applications (IDNA)

License:        BSD and Python and Unicode
URL:            https://github.com/kjd/idna
Source0:        https://pypi.python.org/packages/source/i/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # with_python3

%description
A library to support the Internationalised Domain Names in Applications (IDNA)
protocol as specified in RFC 5891 <http://tools.ietf.org/html/rfc5891>.  This
version of the protocol is often referred to as "IDNA2008" and can produce
different results from the earlier standard from 2003.

The library is also intended to act as a suitable drop-in replacement for the
"encodings.idna" module that comes with the Python standard library but
currently only supports the older 2003 specification.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Internationalized Domain Names in Applications (IDNA)

%description -n python3-%{srcname}
A library to support the Internationalised Domain Names in Applications (IDNA)
protocol as specified in RFC 5891 <http://tools.ietf.org/html/rfc5891>.  This
version of the protocol is often referred to as "IDNA2008" and can produce
different results from the earlier standard from 2003.

The library is also intended to act as a suitable drop-in replacement for the
"encodings.idna" module that comes with the Python standard library but
currently only supports the older 2003 specification.
%endif # with_python3

%prep
%setup -q -n %{srcname}-%{version}
# Remove bundled egg-info
rm -rf %{srcname}.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3



%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
# Set LANG when building with python 3 due to
# https://github.com/kjd/idna/pull/4
LANG=en_US.UTF-8 %{__python3} setup.py build
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
# Set LANG when building with python 3 due to
# https://github.com/kjd/idna/pull/4
LANG=en_US.UTF-8 %{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python2} setup.py install --skip-build --root %{buildroot}

%check
%{__python2} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
# Set LANG when building with python 3 due to
# https://github.com/kjd/idna/pull/4
LANG=en_US.UTF-8 %{__python3} setup.py test
popd
%endif # with_python3


%files
%doc README.rst HISTORY.rst LICENSE.rst
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc README.rst HISTORY.rst LICENSE.rst
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info
%endif # with_python3

%changelog
* Wed Mar 01 2017 Paul Wouters <pwouters@redhat.com> - 2.4-1
- Resolves: rhbz#1425154 (2.3 broke API and upstream released 2.4)

* Tue Feb 28 2017 Paul Wouters <pwouters@redhat.com> - 2.3-1
- Resolves: rhbz#1425154 Rebase python-idna (more memfixes)

* Thu Feb 23 2017 Paul Wouters <pwouters@redhat.com> - 2.2-1
- Resolves: rhbz#1425154 Rebase python-idna to >= 2.1 for freeipa performance issue

* Thu Apr 07 2016 Paul Wouters <pwouters@redhat.com> - 2.0-1
- Resolves: rhbz#1297583 New package: python-idna
