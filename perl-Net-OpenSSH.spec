#
# Conditional build:
%bcond_without	tests		# do not perform "make test"

%define		pdir	Net
%define		pnam	OpenSSH
Summary:	Net::OpenSSH - Perl SSH client package implemented on top of OpenSSH
Name:		perl-Net-OpenSSH
Version:	0.65_05
Release:	2
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-authors/id/S/SA/SALVA/Net-OpenSSH-%{version}.tar.gz
# Source0-md5:	beef8cd48d10e12fc19a2ef836f754a6
URL:		http://search.cpan.org/dist/Net-OpenSSH/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	openssh-clients >= 2:4.1
Suggests:	perl-IO-Tty
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Net::OpenSSH is a secure shell client package implemented on top of
OpenSSH binary client (ssh).

This package is implemented around the multiplexing feature found in
later versions of OpenSSH. That feature allows one to run several
sessions over a single SSH connection (OpenSSH 4.1 was the first one
to provide all the required functionality).

When a new Net::OpenSSH object is created, the OpenSSH ssh client is
run in master mode, establishing a persistent (for the lifetime of the
object) connection to the server.

Then, every time a new operation is requested a new ssh process is
started in slave mode, effectively reusing the master SSH connection
to send the request to the remote side.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a sample/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorlib}/Net/*.pm
%{perl_vendorlib}/Net/OpenSSH
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
