%define defconfig DailySet1
%define indexserver amandahost
%define tapeserver %{indexserver}
%define amanda_user amandabackup
%define amanda_group disk
Summary:	A network-capable tape backup solution
Name:		amanda
Version:	3.2.3
Release:	4
Source0:	http://downloads.sourceforge.net/amanda/amanda-%{version}.tar.gz
Source1:	amanda.crontab
Source4:	disklist
Source5:	amanda-xinetd
Source8:	amandahosts
Patch1:		amanda-3.1.0-example.patch
Patch2:		amanda-3.1.1-xattrs.patch
Patch3:		amanda-3.1.1-tcpport.patch
Patch5:		amanda-3.1.1-bsd.patch
Patch6:		amanda-3.2.0-config-dir.patch
License:	BSD
Group:		Archiving/Backup
URL:		http://www.amanda.org
BuildRequires:	automake autoconf libtool
BuildRequires:	dump gnuplot cups samba-client tar grep
BuildRequires:	gcc-c++ readline-devel
BuildRequires:	krb5-devel netkit-rsh openssh-clients ncompress mtx mt-st
BuildRequires:	perl-devel perl(ExtUtils::Embed) perl(Test::Simple)
BuildRequires:	glib2-devel openssl-devel swig bison flex
BuildRequires:	libcurl-devel
Requires(pre):	shadow-utils
Requires(post):	grep sed
Requires:	grep initscripts tar /bin/mail xinetd
#Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Obsoletes:	amanda-devel < 2.6.1p2-5
Provides:	amanda-devel = 2.6.1p2-5

%global __perl_provides /bin/sh -c "/usr/lib/rpm/perl.prov | grep -v \\\"perl(Math::BigInt)\\\""

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

%package	client
Summary:	The client component of the AMANDA tape backup system
Group:		Archiving/Backup
Requires:	grep /sbin/service
Requires(pre):	amanda = %{version}-%{release}

%description	client
The Amanda-client package should be installed on any machine that will
be backed up by AMANDA (including the server if it also needs to be
backed up).  You will also need to install the amanda package on each
AMANDA client machine.

%package	server
Summary:	The server side of the AMANDA tape backup system
Group:		Archiving/Backup
Requires:	grep /sbin/service
Requires(pre):	amanda = %{version}-%{release}

%description server
The amanda-server package should be installed on the AMANDA server,
the machine attached to the device(s) (such as a tape drive) where backups
will be written. You will also need to install the amanda package on
the AMANDA server machine.  And, if the server is also to be backed up, the
server also needs to have the amanda-client package installed.

%prep
%setup -q
%patch1 -p1 -b .example
%patch2 -p1 -b .xattrs
%patch3 -p1 -b .tcpport
%patch5 -p1 -b .bsd
%patch6 -p1 -b .config
./autogen

%build
%serverbuild
export MAILER=/bin/mail
export CONFIGURE_XPATH=""
%configure2_5x  \
	--enable-shared \
	--disable-rpath \
	--disable-static \
	--disable-dependency-tracking \
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
	--with-user=%amanda_user \
	--with-group=%amanda_group \
	--with-tmpdir=/var/log/amanda \
	--with-gnutar=/bin/tar \
	--with-ssh-security \
	--with-rsh-security \
	--with-bsdtcp-security \
	--with-bsdudp-security \
	--with-krb5-security

%make

%install
%makinstall_std BINARY_OWNER=%(id -un) SETUID_GROUP=%(id -gn)

mkdir -p $RPM_BUILD_ROOT/etc/xinetd.d
cp %SOURCE5 $RPM_BUILD_ROOT/etc/xinetd.d/amanda
chmod 644 $RPM_BUILD_ROOT/etc/xinetd.d/amanda
mkdir -p $RPM_BUILD_ROOT/var/log/amanda
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/amanda
install -m 600 %SOURCE8 $RPM_BUILD_ROOT%{_localstatedir}/lib/amanda/.amandahosts

ln -s %{_libexecdir}/amanda/amandad $RPM_BUILD_ROOT%{_sbindir}/amandad
#ln -s amrecover.8.gz $RPM_BUILD_ROOT%{_mandir}/man8/amoldrecover.8

pushd ${RPM_BUILD_ROOT}
  mv .%{_sysconfdir}/amanda/example .%{_sysconfdir}/amanda/%defconfig
  cp ${RPM_SOURCE_DIR}/amanda.crontab .%{_sysconfdir}/amanda/crontab.sample
  cp ${RPM_SOURCE_DIR}/disklist .%{_sysconfdir}/amanda/%defconfig
  cp ${RPM_SOURCE_DIR}/disklist .%{_sysconfdir}/amanda/%defconfig
  rm -f .%{_sysconfdir}/amanda/%defconfig/xinetd*
  rm -f .%{_sysconfdir}/amanda/%defconfig/inetd*

  mkdir -p .%{_localstatedir}/lib/amanda/gnutar-lists
  mkdir -p .%{_localstatedir}/lib/amanda/%defconfig/index
  touch .%{_localstatedir}/lib/amanda/amandates
popd
rm -rf $RPM_BUILD_ROOT/usr/share/amanda
find $RPM_BUILD_ROOT -name \*.la | xargs rm

%check
make check

%pre
/usr/sbin/useradd -M -N -g %amanda_group -o -r -d %{_localstatedir}/lib/amanda -s /bin/bash \
	-c "Amanda user" -u 33 %amanda_user >/dev/null 2>&1 || :
/usr/bin/gpasswd -a %amanda_user tape >/dev/null 2>&1 || :

%post
[ -f /var/lock/subsys/xinetd ] && /sbin/service xinetd reload > /dev/null 2>&1 || :

%postun
[ -f /var/lock/subsys/xinetd ] && /sbin/service xinetd reload > /dev/null 2>&1 || :

%files
%doc COPYRIGHT* NEWS README
%config(noreplace) /etc/xinetd.d/amanda

%{_libdir}/libamanda-*.so
%{_libdir}/libamanda.so
%{_libdir}/libamandad*.so
%{_libdir}/libamar*.so
%{_libdir}/libamglue*.so
%{_libdir}/libamxfer*.so
%{_libdir}/libndmjob*.so
%{_libdir}/libndmlib*.so

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
%dir %{_sysconfdir}/amanda/%defconfig

%attr(-,%amanda_user,%amanda_group) %dir %{_localstatedir}/lib/amanda/
%attr(600,%amanda_user,%amanda_group) %config(noreplace) %{_localstatedir}/lib/amanda/.amandahosts
%attr(02700,%amanda_user,%amanda_group) %dir /var/log/amanda

%files server
%{_libdir}/libamdevice*.so
%{_libdir}/libamserver*.so
%{_libexecdir}/amanda/amcleanupdisk
%{_libexecdir}/amanda/amcheck-device
%{_libexecdir}/amanda/amidxtaped
%{_libexecdir}/amanda/amindexd
%{_libexecdir}/amanda/amlogroll
%{_libexecdir}/amanda/amtrmidx
%{_libexecdir}/amanda/amtrmlog
%{_libexecdir}/amanda/driver
%attr(4750,root,%amanda_group) %{_libexecdir}/amanda/dumper
%{_libexecdir}/amanda/chg-disk
%{_libexecdir}/amanda/chg-lib.sh
%{_libexecdir}/amanda/chg-manual
%{_libexecdir}/amanda/chg-multi
%{_libexecdir}/amanda/chg-zd-mtx
%{_libexecdir}/amanda/chunker
%attr(4750,root,%amanda_group) %{_libexecdir}/amanda/planner
%{_libexecdir}/amanda/taper
%{_sbindir}/activate-devpay
%{_sbindir}/amaddclient
%{_sbindir}/amadmin
%{_sbindir}/amcleanup
%{_sbindir}/amdevcheck
%{_sbindir}/amdump
%{_sbindir}/amfetchdump
%{_sbindir}/amflush
%attr(4750,root,%amanda_group) %{_sbindir}/amcheck
%{_sbindir}/amcheckdb
%{_sbindir}/amcheckdump
%{_sbindir}/amlabel
%{_sbindir}/amoverview
%{_sbindir}/amreport
%{_sbindir}/amrestore
%{_sbindir}/amrmtape
%{_sbindir}/amserverconfig
%attr(4750,root,%amanda_group) %{_sbindir}/amservice
%{_sbindir}/amstatus
%{_sbindir}/amtape
%{_sbindir}/amtapetype
%{_sbindir}/amtoc
%{_sbindir}/amvault

%{_mandir}/man5/disklist.5*
%{_mandir}/man5/tapelist.5*
%{_mandir}/man7/amanda-devices.7*
%{_mandir}/man7/amanda-changers.7*
%{_mandir}/man7/amanda-taperscan.7*
%{_mandir}/man8/amaddclient.8*
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
%{perl_vendorarch}/Amanda/Interactive/
%{perl_vendorarch}/Amanda/Interactive.pm
%{perl_vendorarch}/Amanda/Logfile.pm
%{perl_vendorarch}/Amanda/Recovery/
%{perl_vendorarch}/Amanda/Report/
%{perl_vendorarch}/Amanda/Report.pm
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
%config(noreplace) %{_sysconfdir}/amanda/%defconfig/*
%exclude %{_sysconfdir}/amanda/%defconfig/amanda-client.conf
%exclude %{_sysconfdir}/amanda/%defconfig/amanda-client-postgresql.conf

%attr(-,%amanda_user,%amanda_group) %dir %{_localstatedir}/lib/amanda/%defconfig/
%attr(-,%amanda_user,%amanda_group) %dir %{_localstatedir}/lib/amanda/%defconfig/index
%attr(-,%amanda_user,%amanda_group) %dir %{_localstatedir}/lib/amanda/template.d
%attr(-,%amanda_user,%amanda_group) %config(noreplace) %{_localstatedir}/lib/amanda/template.d/*

%files client
%{_libdir}/libamclient*.so

%dir %{_libexecdir}/amanda/application/
%attr(4750,root,%amanda_group) %{_libexecdir}/amanda/application/amgtar
%attr(4750,root,%amanda_group) %{_libexecdir}/amanda/application/amstar
%{_libexecdir}/amanda/application/amlog-script
%{_libexecdir}/amanda/application/ampgsql
%{_libexecdir}/amanda/application/amraw
%{_libexecdir}/amanda/application/amsamba
%{_libexecdir}/amanda/application/amsuntar
%{_libexecdir}/amanda/application/amzfs-sendrecv
%{_libexecdir}/amanda/application/amzfs-snapshot
%{_libexecdir}/amanda/application/script-email

%attr(4750,root,%amanda_group) %{_libexecdir}/amanda/calcsize
%attr(4750,root,%amanda_group) %{_libexecdir}/amanda/killpgrp
%{_libexecdir}/amanda/noop
%{_libexecdir}/amanda/patch-system
%attr(4750,root,%amanda_group) %{_libexecdir}/amanda/rundump
%attr(4750,root,%amanda_group) %{_libexecdir}/amanda/runtar
%{_libexecdir}/amanda/selfcheck
%{_libexecdir}/amanda/sendbackup
%{_libexecdir}/amanda/sendsize
%{_libexecdir}/amanda/teecount
%{_sbindir}/amoldrecover
%{_sbindir}/amrecover

%{_mandir}/man7/amanda-applications.7*
%{_mandir}/man5/amanda-client.conf.5*
%{_mandir}/man8/amgtar.8*
%{_mandir}/man8/ampgsql.8*
%{_mandir}/man8/amraw.8*
%{_mandir}/man8/amrecover.8*
#%{_mandir}/man8/amoldrecover.8*
%{_mandir}/man8/amsamba.8*
%{_mandir}/man8/amstar.8*
%{_mandir}/man8/amsuntar.8*
%{_mandir}/man8/amzfs-sendrecv.8*
%{_mandir}/man8/amzfs-snapshot.8*

%{perl_vendorarch}/Amanda/Application.pm
%{perl_vendorarch}/Amanda/Application/
%{perl_vendorarch}/auto/Amanda/Application/

%config(noreplace) %{_sysconfdir}/amanda/%defconfig/amanda-client.conf
%config(noreplace) %{_sysconfdir}/amanda/%defconfig/amanda-client-postgresql.conf

%attr(-,%amanda_user,%amanda_group) %config(noreplace) %{_localstatedir}/lib/amanda/amandates
%attr(-,%amanda_user,%amanda_group) %{_localstatedir}/lib/amanda/gnutar-lists/


%changelog
* Mon Aug 22 2011 Alexander Khryukin <alexander@mezon.ru> 3.2.3-1mdv2011.0
+ Revision: n\a
- Version bump to 3.2.3
  + Alexander Khryukin
    - spec file merged with spec from fedora and added mandriva fixes

* Mon Sep 29 2008 Oden Eriksson <oeriksson@mandriva.com> 2.5.1-8mdv2009.0
+ Revision: 289339
- fix linkage

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Dec 14 2007 Thierry Vignaud <tvignaud@mandriva.com> 2.5.1-5mdv2008.1
+ Revision: 119836
- rebuild b/c of missing subpackage on ia32

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 2.5.1-4mdv2008.0
+ Revision: 83526
- new devel naming


* Thu Mar 01 2007 Emmanuel Andry <eandry@mandriva.org> 2.5.1-3mdv2007.0
+ Revision: 130266
- rebuild for libintl

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against new libintl major (8)

* Fri Dec 22 2006 Oden Eriksson <oeriksson@mandriva.com> 2.5.1-1mdv2007.1
+ Revision: 101529
- Import amanda

* Sun Sep 17 2006 Oden Eriksson <oeriksson@mandriva.com> 2.5.1-1mdv2007.0
- 2.5.1
- deactivated P5 as it needs to be updated (DVD support)
- added P7 from the sf tracker

* Wed Aug 23 2006 Oden Eriksson <oeriksson@mandriva.com> 2.5.0-2mdv2007.0
- 2.5.0-p2
- fix deps

* Tue Mar 28 2006 Oden Eriksson <oeriksson@mandriva.com> 2.5.0-1mdk
- 2.5.0
- rediffed P3,P4,P5
- dropped P2

* Sun Mar 12 2006 Oden Eriksson <oeriksson@mandriva.com> 2.4.5p1-1mdk
- 2.4.5p1
- rediffed P3
- added the dvd patch (P5)
- added one silly lib64 fix
- fixed the xinetd restart (duh!)

* Thu May 05 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.4.5-2mdk
- added P3 to stop setting chown and suid bits
- use the %%mkrel macro

* Mon Apr 25 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.4.5-1mdk
- 2.4.5

* Fri Feb 04 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.4.4p4-3mdk
- rebuilt against new readline

* Fri Dec 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.4.4p4-2mdk
- added P3 to make it build on 10.0 (thanks pld!)

* Fri Dec 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.4.4p4-1mdk
- 2.4.4p4

* Sat Jul 03 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.4.4p3-1mdk
- 2.4.4p3

* Fri May 21 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.4.4p2-2mdk
- added P2 (fedora)
- fix deps

* Tue May 18 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.4.4p2-1mdk
- 2.4.4p2
- fix soname
- use the %%configure2_5x macro
- misc spec file fixes

