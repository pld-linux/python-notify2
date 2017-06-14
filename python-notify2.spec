#
# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module		notify2
%define 	egg_name	notify2
%define		pypi_name	notify2
Summary:	Python 2 interface to DBus notifications
Name:		python-%{pypi_name}
Version:	0.3.1
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/n/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	ffccaed9330787c7442b453f6520a474
URL:		https://bitbucket.org/takluyver/pynotify2
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	sphinx-pdg
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
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
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/%{pypi_name}.py[co]
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%{py3_sitescriptdir}/%{pypi_name}.py
%{py3_sitescriptdir}/__pycache__/*.pyc
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc html
%endif
