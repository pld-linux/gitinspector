#
# Conditional build:
%bcond_without	doc		# don't build doc

Summary:	Statistical analysis tool for git repositories
Name:		gitinspector
Version:	0.3.2
Release:	1
License:	GPL v3
Group:		Development/Tools
Source0:	https://gitinspector.googlecode.com/files/%{name}_%{version}.zip
# Source0-md5:	e1cbc2c5883c161f0deab8eb4cf025ad
# https://code.google.com/p/gitinspector/issues/detail?id=29
Patch0:		%{name}-lang-c.diff
URL:		https://code.google.com/p/gitinspector/
BuildRequires:	git-core
BuildRequires:	python-distribute
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	unzip
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gitinspector is a statistical analysis tool for git repositories. The
defaut analysis shows general statistics per author, which can be
complemented with a timeline analysis that shows the workload and
activity of each author. Under normal operation, it filters the
results to only show statistics about a number of given extensions and
by default only includes source files in the statistical analysis.

%prep
%setup -q
%patch0 -p1

%build
%{__python} setup.py build --build-base build-2 %{?with_tests:test}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}/translations/messages.pot
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}/translations/*.po
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/gitinspector

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt DESCRIPTION.txt LICENSE.txt
%attr(755,root,root) %{_bindir}/gitinspector
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/*.py[co]
%dir %{py_sitescriptdir}/%{name}/translations
%lang(it) %{py_sitescriptdir}/%{name}/translations/messages_it.mo
%lang(pl) %{py_sitescriptdir}/%{name}/translations/messages_pl.mo
%lang(sv) %{py_sitescriptdir}/%{name}/translations/messages_sv.mo
%lang(zh_TW) %{py_sitescriptdir}/%{name}/translations/messages_zh.mo
%{py_sitescriptdir}/%{name}-%{version}-py*.egg-info

%dir %{py_sitescriptdir}/%{name}/html
%{py_sitescriptdir}/%{name}/html/gitinspector_piclet.png
%{py_sitescriptdir}/%{name}/html/html.footer
%{py_sitescriptdir}/%{name}/html/html.header

# TODO: externalize?
%{py_sitescriptdir}/%{name}/html/flot.zip
%{py_sitescriptdir}/%{name}/html/jquery.tablesorter.min.js.zip
