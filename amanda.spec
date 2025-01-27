%define _disable_ld_no_undefined 1

# new perl policy
%if %{_use_internal_dependency_generator}
%define __noautoprov 'perl\\(Math::BigInt\\)'
%else
%define _provides_exceptions perl(Math::BigInt)
%endif

%define defconfig DailySet1
%define indexserver amandahost
%define tapeserver %{indexserver}
%define amanda_user amandabackup
%define amanda_group disk

Summary:	A network-capable tape backup solution
Name:		amanda
Version:	3.3.5
Release:	3
License:	BSD
Group:		Archiving/Backup
Url:		https://www.amanda.org
Source0:	http://downloads.sourceforge.net/amanda/amanda-%{version}.tar.gz
Source1:	amanda.crontab
Source4:	disklist
Source5:	amanda-xinetd
Source8:	amandahosts
# filter server spcific permits
Source100:	%{name}.rpmlintrc
Patch2:		amanda-3.1.1-xattrs.patch
Patch3:		amanda-3.1.1-tcpport.patch
Patch6:		amanda-3.2.0-config-dir.patch
Patch11:	amanda-3.3.0-kerberos5-deprecated.patch
BuildRequires:	dump
BuildRequires:	gnuplot
BuildRequires:	cups
BuildRequires:	samba-client
BuildRequires:	krb5-devel
BuildRequires:	netkit-rsh
BuildRequires:	openssh-clients
BuildRequires:	ncompress mtx mt-st
BuildRequires:	perl-devel
BuildRequires:	perl(ExtUtils::Embed)
BuildRequires:	perl(Test::Simple)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	swig
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	readline-devel
BuildRequires:	gettext-devel

Requires(pre):	shadow-utils
Requires:	xinetd
%rename		amanda-devel

%description
AMANDA, the Advanced Maryland Automatic Network Disk Archiver, is a
backup system that allows the administrator of a LAN to set up a
single master backup server to back up multiple hosts to one or more
tape drives or disk files.  AMANDA uses native dump and/or GNU tar
facilities and can back up a large number of workstations running
multiple versions of Unix.  Newer versions of AMANDA (including this
version) can use SAMBA to back up Microsoft(TM) Windows95/NT hosts.
The amanda package contains the core AMANDA programs and will need to
be installed on both AMANDA clients and AMANDA servers.  Note that you
will have to install the amanda-client and/or amanda-server packages as
well.

%files
%doc COPYRIGHT* NEWS README
%config(noreplace) %{_sysconfdir}/xinetd.d/amanda
%dir %{_libexecdir}/amanda
%{_libexecdir}/amanda/amandad
%{_libexecdir}/amanda/amanda-sh-lib.sh
%{_libexecdir}/amanda/amcat.awk
%{_libexecdir}/amanda/amndmjob
%{_libexecdir}/amanda/amplot.awk
%{_libexecdir}/amanda/amplot.g
%{_libexecdir}/amanda/amplot.gp
%{_libexecdir}/amanda/ndmjob

%{_sbindir}/amandad
%{_sbindir}/amaespipe
%{_sbindir}/amarchiver
%{_sbindir}/amcrypt
%{_sbindir}/amcrypt-ossl
%{_sbindir}/amcrypt-ossl-asym
%{_sbindir}/amcryptsimple
%{_sbindir}/amgetconf
%{_sbindir}/amgpgcrypt
%{_sbindir}/amplot

%{perl_vendorarch}/Amanda/Archive.pm
%{perl_vendorarch}/Amanda/BigIntCompat.pm
%{perl_vendorarch}/Amanda/ClientService.pm
%{perl_vendorarch}/Amanda/Config.pm
%{perl_vendorarch}/Amanda/Config/
%{perl_vendorarch}/Amanda/Constants.pm
%{perl_vendorarch}/Amanda/Debug.pm
# Extract.pm
%{perl_vendorarch}/Amanda/Extract.pm
#
%{perl_vendorarch}/Amanda/Feature.pm
%{perl_vendorarch}/Amanda/Header.pm
%{perl_vendorarch}/Amanda/IPC
%{perl_vendorarch}/Amanda/MainLoop.pm
%{perl_vendorarch}/Amanda/NDMP.pm
%{perl_vendorarch}/Amanda/Paths.pm
%{perl_vendorarch}/Amanda/Process.pm
%{perl_vendorarch}/Amanda/Script_App.pm
%{perl_vendorarch}/Amanda/Script.pm
%{perl_vendorarch}/Amanda/Tests.pm
%{perl_vendorarch}/Amanda/Util.pm
%{perl_vendorarch}/Amanda/Xfer.pm
%{perl_vendorarch}/auto/Amanda/Archive/
%{perl_vendorarch}/auto/Amanda/Config/
%{perl_vendorarch}/auto/Amanda/Debug/
%{perl_vendorarch}/auto/Amanda/Feature/
%{perl_vendorarch}/auto/Amanda/Header/
%{perl_vendorarch}/auto/Amanda/IPC/
%{perl_vendorarch}/auto/Amanda/MainLoop/
%{perl_vendorarch}/auto/Amanda/NDMP/
%{perl_vendorarch}/auto/Amanda/Tests/
%{perl_vendorarch}/auto/Amanda/Util/
%{perl_vendorarch}/auto/Amanda/Xfer/

%{_mandir}/man5/amanda-archive-format.5*
%{_mandir}/man7/amanda-compatibility.7*
%{_mandir}/man5/amanda.conf*
%{_mandir}/man7/amanda-auth.7*
%{_mandir}/man7/amanda-match.7*
%{_mandir}/man7/amanda-scripts.7*
%{_mandir}/man8/amanda.8*
%{_mandir}/man8/amarchiver.8*
%{_mandir}/man8/amplot.8*
%{_mandir}/man8/script-email.8*
%{_mandir}/man8/amaespipe.8*
%{_mandir}/man8/amcrypt-ossl-asym.8*
%{_mandir}/man8/amcrypt-ossl.8*
%{_mandir}/man8/amcryptsimple.8*
%{_mandir}/man8/amcrypt.8*
%{_mandir}/man8/amgpgcrypt.8*
%{_mandir}/man8/amgetconf.8*

%dir %{_sysconfdir}/amanda/
%dir %{_sysconfdir}/amanda/%{defconfig}

%attr(-,%{amanda_user},%{amanda_group}) %dir %{_localstatedir}/lib/amanda/
%attr(600,%{amanda_user},%{amanda_group}) %config(noreplace) %{_localstatedir}/lib/amanda/.amandahosts
%attr(02700,%{amanda_user},%{amanda_group}) %dir %{_var}/log/amanda

%pre
/usr/sbin/useradd -M -N -g %{amanda_group} -o -r -d %{_localstatedir}/lib/amanda -s /bin/bash \
	-c "Amanda user" -u 33 %{amanda_user} >/dev/null 2>&1 || :
/usr/bin/gpasswd -a %{amanda_user} tape >/dev/null 2>&1 || :

%post
[ -f %{_var}/lock/subsys/xinetd ] && /sbin/service xinetd reload > /dev/null 2>&1 || :

%postun
[ -f %{_var}/lock/subsys/xinetd ] && /sbin/service xinetd reload > /dev/null 2>&1 || :

#----------------------------------------------------------------------------

%package	client
Summary:	The client component of the AMANDA tape backup system
Group:		Archiving/Backup
Requires:	amanda = %{EVRD}

%description	client
The Amanda-client package should be installed on any machine that will
be backed up by AMANDA (including the server if it also needs to be
backed up).  You will also need to install the amanda package on each
AMANDA client machine.

%files client
%doc COPYRIGHT* NEWS README
%dir %{_libexecdir}/amanda/application/
%attr(4750,root,%{amanda_group}) %{_libexecdir}/amanda/application/amgtar
%attr(4750,root,%{amanda_group}) %{_libexecdir}/amanda/application/amstar
%{_libexecdir}/amanda/application/amlog-script
%{_libexecdir}/amanda/application/ampgsql
%{_libexecdir}/amanda/application/amraw
%{_libexecdir}/amanda/application/amsamba
%{_libexecdir}/amanda/application/amsuntar
%{_libexecdir}/amanda/application/amzfs-sendrecv
%{_libexecdir}/amanda/application/amzfs-snapshot
%{_libexecdir}/amanda/application/script-email

%attr(4750,root,%{amanda_group}) %{_libexecdir}/amanda/calcsize
%attr(4750,root,%{amanda_group}) %{_libexecdir}/amanda/killpgrp
%{_libexecdir}/amanda/noop
%{_libexecdir}/amanda/patch-system
%attr(4750,root,%{amanda_group}) %{_libexecdir}/amanda/rundump
%attr(4750,root,%{amanda_group}) %{_libexecdir}/amanda/runtar
%{_libexecdir}/amanda/selfcheck
%{_libexecdir}/amanda/sendbackup
%{_libexecdir}/amanda/sendsize
%{_libexecdir}/amanda/teecount
%{_sbindir}/amdump_client
%{_sbindir}/amoldrecover
%{_sbindir}/amrecover

%{_mandir}/man7/amanda-applications.7*
%{_mandir}/man8/amdump_client.8*
%{_mandir}/man5/amanda-client.conf.5*
%{_mandir}/man8/amgtar.8*
%{_mandir}/man8/ampgsql.8*
%{_mandir}/man8/amraw.8*
%{_mandir}/man8/amrecover.8*
%{_mandir}/man8/amsamba.8*
%{_mandir}/man8/amstar.8*
%{_mandir}/man8/amsuntar.8*
%{_mandir}/man8/amzfs-sendrecv.8*
%{_mandir}/man8/amzfs-snapshot.8*

%{perl_vendorarch}/Amanda/Application.pm
%{perl_vendorarch}/Amanda/Application/
%{perl_vendorarch}/auto/Amanda/Application/

%config(noreplace) %{_sysconfdir}/amanda/%{defconfig}/amanda-client.conf
%config(noreplace) %{_sysconfdir}/amanda/%{defconfig}/amanda-client-postgresql.conf

%attr(-,%{amanda_user},%{amanda_group}) %config(noreplace) %{_localstatedir}/lib/amanda/amandates
%attr(-,%{amanda_user},%{amanda_group}) %{_localstatedir}/lib/amanda/gnutar-lists/

#----------------------------------------------------------------------------

%package	server
Summary:	The server side of the AMANDA tape backup system
Group:		Archiving/Backup
Requires:	amanda = %{EVRD}

%description server
The amanda-server package should be installed on the AMANDA server,
the machine attached to the device(s) (such as a tape drive) where backups
will be written. You will also need to install the amanda package on
the AMANDA server machine.  And, if the server is also to be backed up, the
server also needs to have the amanda-client package installed.

%files server
%doc COPYRIGHT* NEWS README
%{_libexecdir}/amanda/amdumpd
%{_libexecdir}/amanda/amcheck-device
%{_libexecdir}/amanda/amidxtaped
%{_libexecdir}/amanda/amindexd
%{_libexecdir}/amanda/amlogroll
%{_libexecdir}/amanda/amtrmidx
%{_libexecdir}/amanda/amtrmlog
%{_libexecdir}/amanda/driver
%attr(4750,root,%{amanda_group}) %{_libexecdir}/amanda/dumper
%{_libexecdir}/amanda/chg-disk
%{_libexecdir}/amanda/chg-lib.sh
%{_libexecdir}/amanda/chg-manual
%{_libexecdir}/amanda/chg-multi
%{_libexecdir}/amanda/chg-zd-mtx
%{_libexecdir}/amanda/chunker
%attr(4750,root,%{amanda_group}) %{_libexecdir}/amanda/planner
%{_libexecdir}/amanda/taper
%{_sbindir}/activate-devpay
%{_sbindir}/amaddclient
%{_sbindir}/amcleanupdisk
%{_sbindir}/amadmin
%{_sbindir}/amcleanup
%{_sbindir}/amdevcheck
%{_sbindir}/amdump
%{_sbindir}/amfetchdump
%{_sbindir}/amflush
%attr(4750,root,%{amanda_group}) %{_sbindir}/amcheck
%{_sbindir}/amcheckdb
%{_sbindir}/amcheckdump
%{_sbindir}/amlabel
%{_sbindir}/amoverview
%{_sbindir}/amreport
%{_sbindir}/amrestore
%{_sbindir}/amrmtape
%{_sbindir}/amserverconfig
%attr(4750,root,%{amanda_group}) %{_sbindir}/amservice
%{_sbindir}/amstatus
%{_sbindir}/amtape
%{_sbindir}/amtapetype
%{_sbindir}/amtoc
%{_sbindir}/amvault

%{_mandir}/man5/disklist.5*
%{_mandir}/man5/tapelist.5*
%{_mandir}/man7/amanda-devices.7*
%{_mandir}/man7/amanda-changers.7*
%{_mandir}/man7/amanda-interactivity.7*
%{_mandir}/man7/amanda-taperscan.7*
%{_mandir}/man8/amaddclient.8*
%{_mandir}/man8/amcleanupdisk.8.*
%{_mandir}/man8/amadmin.8*
%{_mandir}/man8/amcleanup.8*
%{_mandir}/man8/amdevcheck.8*
%{_mandir}/man8/amdump.8*
%{_mandir}/man8/amfetchdump.8*
%{_mandir}/man8/amflush.8*
%{_mandir}/man8/amcheckdb.8*
%{_mandir}/man8/amcheckdump.8*
%{_mandir}/man8/amcheck.8*
%{_mandir}/man8/amlabel.8*
%{_mandir}/man8/amoverview.8*
%{_mandir}/man8/amreport.8*
%{_mandir}/man8/amrestore.8*
%{_mandir}/man8/amrmtape.8*
%{_mandir}/man8/amserverconfig.8*
%{_mandir}/man8/amservice.8*
%{_mandir}/man8/amstatus.8*
%{_mandir}/man8/amtapetype.8*
%{_mandir}/man8/amtape.8*
%{_mandir}/man8/amtoc.8*
%{_mandir}/man8/amvault.8*

%{perl_vendorarch}/Amanda/Cmdline.pm
%{perl_vendorarch}/Amanda/Curinfo/
%{perl_vendorarch}/Amanda/Curinfo.pm
%{perl_vendorarch}/Amanda/DB/
%{perl_vendorarch}/Amanda/Device.pm
%{perl_vendorarch}/Amanda/Disklist.pm
%{perl_vendorarch}/Amanda/Holding.pm
%{perl_vendorarch}/Amanda/Changer/
%{perl_vendorarch}/Amanda/Changer.pm
%{perl_vendorarch}/Amanda/Interactivity/
%{perl_vendorarch}/Amanda/Interactivity.pm
%{perl_vendorarch}/Amanda/Logfile.pm
%{perl_vendorarch}/Amanda/Recovery/
%{perl_vendorarch}/Amanda/Report/
%{perl_vendorarch}/Amanda/Report.pm
%{perl_vendorarch}/Amanda/ScanInventory.pm
%{perl_vendorarch}/Amanda/Tapelist.pm
%{perl_vendorarch}/Amanda/Taper/
%{perl_vendorarch}/Amanda/XferServer.pm
%{perl_vendorarch}/auto/Amanda/Cmdline/
%{perl_vendorarch}/auto/Amanda/Device/
%{perl_vendorarch}/auto/Amanda/Disklist/
%{perl_vendorarch}/auto/Amanda/Logfile/
%{perl_vendorarch}/auto/Amanda/Tapelist/
%{perl_vendorarch}/auto/Amanda/XferServer/

%config(noreplace) %{_sysconfdir}/amanda/crontab.sample
%config(noreplace) %{_sysconfdir}/amanda/%{defconfig}/*
%exclude %{_sysconfdir}/amanda/%{defconfig}/amanda-client.conf
%exclude %{_sysconfdir}/amanda/%{defconfig}/amanda-client-postgresql.conf

%attr(-,%{amanda_user},%{amanda_group}) %dir %{_localstatedir}/lib/amanda/%{defconfig}/
%attr(-,%{amanda_user},%{amanda_group}) %dir %{_localstatedir}/lib/amanda/%{defconfig}/index
%attr(-,%{amanda_user},%{amanda_group}) %dir %{_localstatedir}/lib/amanda/template.d
%attr(-,%{amanda_user},%{amanda_group}) %config(noreplace) %{_localstatedir}/lib/amanda/template.d/*

#----------------------------------------------------------------------------

%define libamanda %mklibname amanda %{version}

%package -n	%{libamanda}
Summary:	Amanda libamanda library
Group:		System/Libraries

%description -n	%{libamanda}
Amanda libamanda library.

%files -n %{libamanda}
%doc COPYRIGHT* NEWS README
%{_libdir}/libamanda-%{version}.so
%{_libdir}/libamanda.so

#----------------------------------------------------------------------------

%define libamandad %mklibname amandad %{version}

%package -n	%{libamandad}
Summary:	Amanda libamandad library
Group:		System/Libraries

%description -n	%{libamandad}
Amanda libamandad library.

%files -n %{libamandad}
%doc COPYRIGHT* NEWS README
%{_libdir}/libamandad-%{version}.so
%{_libdir}/libamandad.so

#----------------------------------------------------------------------------

%define libamar %mklibname amar %{version}

%package -n	%{libamar}
Summary:	Amanda libamar library
Group:		System/Libraries

%description -n	%{libamar}
Amanda libamar library.

%files -n %{libamar}
%doc COPYRIGHT* NEWS README
%{_libdir}/libamar-%{version}.so
%{_libdir}/libamar.so

#----------------------------------------------------------------------------

%define libamglue %mklibname amglue %{version}

%package -n	%{libamglue}
Summary:	Amanda libamglue library
Group:		System/Libraries

%description -n	%{libamglue}
Amanda libamglue library.

%files -n %{libamglue}
%doc COPYRIGHT* NEWS README
%{_libdir}/libamglue-%{version}.so
%{_libdir}/libamglue.so

#----------------------------------------------------------------------------

%define libamxfer %mklibname amxfer %{version}

%package -n	%{libamxfer}
Summary:	Amanda libamxfer library
Group:		System/Libraries

%description -n	%{libamxfer}
Amanda libamxfer library.

%files -n %{libamxfer}
%doc COPYRIGHT* NEWS README
%{_libdir}/libamxfer-%{version}.so
%{_libdir}/libamxfer.so

#----------------------------------------------------------------------------

%define libndmjob %mklibname ndmjob %{version}

%package -n	%{libndmjob}
Summary:	Amanda libndmjob library
Group:		System/Libraries

%description -n	%{libndmjob}
Amanda libndmjob library.

%files -n %{libndmjob}
%doc COPYRIGHT* NEWS README
%{_libdir}/libndmjob-%{version}.so
%{_libdir}/libndmjob.so

#----------------------------------------------------------------------------

%define libndmlib %mklibname ndmlib %{version}

%package -n	%{libndmlib}
Summary:	Amanda libndmlib library
Group:		System/Libraries

%description -n	%{libndmlib}
Amanda libndmlib library.

%files -n %{libndmlib}
%doc COPYRIGHT* NEWS README
%{_libdir}/libndmlib-%{version}.so
%{_libdir}/libndmlib.so

#----------------------------------------------------------------------------

%define libamdevice %mklibname amdevice %{version}

%package -n	%{libamdevice}
Summary:	Amanda libamdevice library
Group:		System/Libraries

%description -n	%{libamdevice}
Amanda libamdevice library.

%files -n %{libamdevice}
%doc COPYRIGHT* NEWS README
%{_libdir}/libamdevice-%{version}.so
%{_libdir}/libamdevice.so

#----------------------------------------------------------------------------

%define libamserver %mklibname amserver %{version}

%package -n	%{libamserver}
Summary:	Amanda libamserver library
Group:		System/Libraries

%description -n	%{libamserver}
Amanda libamserver library.

%files -n %{libamserver}
%doc COPYRIGHT* NEWS README
%{_libdir}/libamserver-%{version}.so
%{_libdir}/libamserver.so

#----------------------------------------------------------------------------

%define libamclient %mklibname amclient %{version}

%package -n	%{libamclient}
Summary:	Amanda libamclient library
Group:		System/Libraries

%description -n	%{libamclient}
Amanda libamclient library.

%files -n %{libamclient}
%doc COPYRIGHT* NEWS README
%{_libdir}/libamclient-%{version}.so
%{_libdir}/libamclient.so

#----------------------------------------------------------------------------

%prep
%setup -q
%patch2 -p1 -b .xattrs~
%patch3 -p1 -b .tcpport~
%patch6 -p1 -b .config~
%patch11 -p1 -b .krb5_deprecated~
#./autogen
autoreconf -fi

%build
%serverbuild
export MAILER=/bin/mail
export CONFIGURE_XPATH=""
%configure2_5x \
	--enable-shared \
	--disable-rpath \
	--disable-static \
	--disable-installperms \
	--program-prefix=%{?_program_prefix} \
	--with-amdatadir=%{_localstatedir}/lib/amanda \
	--with-amlibdir=%{_libdir} \
	--with-amperldir=%{perl_vendorarch} \
	--with-index-server=%{indexserver} \
	--with-tape-server=%{tapeserver} \
	--with-config=%{defconfig} \
	--with-gnutar-listdir=%{_localstatedir}/lib/amanda/gnutar-lists \
	--with-smbclient=%{_bindir}/smbclient \
	--with-amandates=%{_localstatedir}/lib/amanda/amandates \
	--with-amandahosts \
	--with-user=%{amanda_user} \
	--with-group=%{amanda_group} \
	--with-tmpdir=%{_var}/log/amanda \
	--with-gnutar=/bin/tar \
	--with-ssh-security \
	--with-rsh-security \
	--with-bsdtcp-security \
	--with-bsdudp-security \
	--with-krb5-security

%make

%install
%makeinstall_std BINARY_OWNER=%(id -un) SETUID_GROUP=%(id -gn)

install -m644 %{SOURCE5} -D %{buildroot}%{_sysconfdir}/xinetd.d/amanda
mkdir -p %{buildroot}%{_var}/log/amanda
install -m600 %{SOURCE8} -D %{buildroot}%{_localstatedir}/lib/amanda/.amandahosts

ln -s %{_libexecdir}/amanda/amandad %{buildroot}%{_sbindir}/amandad

mkdir -p %{buildroot}%{_sysconfdir}/amanda
mv %{buildroot}%{_localstatedir}/lib/amanda/example %{buildroot}%{_sysconfdir}/amanda/%{defconfig}
install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/amanda/crontab.sample
install -m644 %{SOURCE4} -D %{buildroot}%{_sysconfdir}/amanda/%{defconfig}
rm -f %{buildroot}%{_sysconfdir}/amanda/%{defconfig}/xinetd*
rm -f %{buildroot}%{_sysconfdir}/amanda/%{defconfig}/inetd*

mkdir -p %{buildroot}%{_localstatedir}/lib/amanda/gnutar-lists
mkdir -p %{buildroot}%{_localstatedir}/lib/amanda/%{defconfig}/index
touch %{buildroot}%{_localstatedir}/lib/amanda/amandates

rm -rf %{buildroot}%{_datadir}/amanda

