#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		notify2
%define		egg_name	notify2
%define		pypi_name	notify2
Summary:	Python 2 interface to DBus notifications
Name:		python-%{pypi_name}
Version:	0.3.1
Release:	7
License:	BSD
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/n/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	ffccaed9330787c7442b453f6520a474
URL:		https://bitbucket.org/takluyver/pynotify2
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
%if %{with doc}
BuildRequires:	python3-devel-tools
BuildRequires:	sphinx-pdg
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a pure Python replacement for notify-python, using python-dbus
to communicate with the notifications server directly.

%package -n python3-%{pypi_name}
Summary:	Python 3 interface to DBus notifications
Group:		Libraries/Python

%description -n python3-%{pypi_name}
This is a pure Python replacement for notify-python, using python-dbus
to communicate with the notifications server directly.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%if %{with doc}
# generate html docs
sphinx-build docs html
# remove the sphinx-build leftovers
%{__rm} -r html/.{doctrees,buildinfo}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
%{__rm} $RPM_BUILD_ROOT%{_examplesdir}/python-%{pypi_name}-%{version}/notify2.py
%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python(\s|$),#!%{__python}\1,' \
	$RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}/*.py
%endif

%if %{with python3}
%py3_install
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{pypi_name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{pypi_name}-%{version}
%{__rm} $RPM_BUILD_ROOT%{_examplesdir}/python3-%{pypi_name}-%{version}/notify2.py
%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python(\s|$),#!%{__python3}\1,' \
	$RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}/*.py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/%{pypi_name}.py[co]
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{_examplesdir}/python-%{module}-%{version}
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%{py3_sitescriptdir}/%{pypi_name}.py
%{py3_sitescriptdir}/__pycache__/*.pyc
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{pypi_name}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc html/*
%endif
