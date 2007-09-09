# OE 20040517: define soname (used right after %%setup)
%define amanda_version_info 2:5:2

%define major 0
%define libname %mklibname amanda %{major}
%define develname %mklibname amanda -d

%define	_libexecdir %{_libdir}/amanda
%define plevel %{nil}

Summary:	A network-capable tape backup solution
Name:		amanda
Version:	2.5.1
Release:	%mkrel 4
License:	BSD
Group:		Archiving/Backup
URL:		http://www.amanda.org
Source0:	http://download.sourceforge.net/amanda/amanda-%{version}%{plevel}.tar.bz2
Source1:	amanda.crontab.bz2
Source2:	__README_QUICKSETUP__.bz2
Source3:	amanda.conf.bz2
Source4:	disklist.bz2
Source5:	amanda-xinetd.bz2
Source6:	amandaidx-xinetd.bz2
Source7:	amidxtape-xinetd.bz2
Source8:	amandahosts.bz2
Source9:	amanda.pdf
Patch0:		amanda-2.4.2-bug18322.patch
Patch1:		amanda-2.4.2p2-append.patch
Patch3:		amanda-2.5.0-no_private_libtool.m4.diff
Patch4:		amanda-2.5.0-no_uid_gid_suid_install.diff
Patch5:		amanda-2.5.0-dvd.diff
Patch6:		amanda-2.5.0-perlbang.diff
Patch7:		amanda-2.5.1-ubuntu.diff
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	libtool
BuildRequires:	cups-common
BuildRequires:	dump
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	gnuplot
BuildRequires:	libtermcap-devel
BuildRequires:	mailx
BuildRequires:	mt-st
BuildRequires:	mtx
BuildRequires:	openssh-clients
BuildRequires:	readline-devel
BuildRequires:	samba-client
BuildRequires:	xfsdump
BuildRequires:	openssl-devel
ExcludeArch:	ia64
Requires:	tar >= 1.15
Requires:	libtermcap
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description 
AMANDA, the Advanced Maryland Automatic Network Disk Archiver, is a
backup system that allows the administrator of a LAN to set up a single
master backup server to back up multiple hosts to a single large capacity
tape drive.  AMANDA uses native dump and/or GNU tar facilities and can
back up a large number of workstations running multiple versions of Unix.
Newer versions of AMANDA (including this version) can use SAMBA to back
up Microsoft(TM) Windows95/NT hosts.  The amanda package contains the
core AMANDA programs and will need to be installed on both AMANDA clients
and AMANDA servers.  Note that you will have to install the amanda-client
and amanda-server packages as well.

%package	client
Summary:	The client component of the AMANDA tape backup system
Group:		Archiving/Backup
Requires:	openssh-clients
Requires:	xinetd

%description	client
The Amanda-client package should be installed on any machine that will
be backed up by AMANDA (including the server if it also needs to be
backed up).  You will also need to install the amanda package to each
AMANDA client.

%package	server
Summary:	The server side of the AMANDA tape backup system
Group:		Archiving/Backup
Requires:	gnuplot
Requires:	mailx
Requires:	mt-st
Requires:	openssh-clients
Requires:	openssh-server
Requires:	xinetd

%description	server
The amanda-server package should be installed on the AMANDA server,
the machine attached to the device (such as a tape drive) where backups
will be written. You will also need to install the amanda package to
the AMANDA server.  And, if the server is also to be backed up, the
server also needs to have the amanda-client package installed.

%package -n	%{libname}
Summary:	Libraries and documentation of the AMANDA tape backup system
Group:		Archiving/Backup
Requires:	tar
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
AMANDA, the Advanced Maryland Automatic Network Disk Archiver, is a
backup system that allows the administrator of a LAN to set up a single
master backup server to back up multiple hosts to a single large capacity
tape drive.  AMANDA uses native dump and/or GNU tar facilities and can
back up a large number of workstations running multiple versions of Unix.
Newer versions of AMANDA (including this version) can use SAMBA to back
up Microsoft(TM) Windows95/NT hosts.  The amanda package contains the
core AMANDA programs and will need to be installed on both AMANDA clients
and AMANDA servers.  Note that you will have to install the amanda-client

%package -n	%{libname}-client
Summary:	Libraries for amanda client
Group:		System/Libraries
Provides:	lib%{name}-client = %{version}-%{release}
# urpmi help
Conflicts:	amanda-client <= 2.4.4-1mdk

%description -n %{libname}-client
AMANDA, the Advanced Maryland Automatic Network Disk Archiver, is a
backup system that allows the administrator of a LAN to set up a single
master backup server to back up multiple hosts to a single large capacity
tape drive.  AMANDA uses native dump and/or GNU tar facilities and can
back up a large number of workstations running multiple versions of Unix.
Newer versions of AMANDA (including this version) can use SAMBA to back
up Microsoft(TM) Windows95/NT hosts.  The amanda package contains the
core AMANDA programs and will need to be installed on both AMANDA clients
and AMANDA servers.  Note that you will have to install the amanda-client

%package -n	%{libname}-server
Summary:	Libraries for amanda-server
Group:		System/Libraries
Provides:	lib%{name}-server = %{version}-%{release}
# urpmi help
Conflicts:	amanda-server <= 2.4.4-1mdk

%description -n %{libname}-server
AMANDA, the Advanced Maryland Automatic Network Disk Archiver, is a
backup system that allows the administrator of a LAN to set up a single
master backup server to back up multiple hosts to a single large capacity
tape drive.  AMANDA uses native dump and/or GNU tar facilities and can
back up a large number of workstations running multiple versions of Unix.
Newer versions of AMANDA (including this version) can use SAMBA to back
up Microsoft(TM) Windows95/NT hosts.  The amanda package contains the
core AMANDA programs and will need to be installed on both AMANDA clients
and AMANDA servers.  Note that you will have to install the amanda-client

%package -n	%{develname}
Summary:	Libraries and documentation of the AMANDA tape backup system
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libname}-server = %{version}-%{release}
Requires:	%{libname}-client = %{version}-%{release}
Provides:	amanda-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname amanda 0 -d}

%description -n %{develname}
The libamanda-devel package should be installed on any machine that will
be used to develop amanda applications.

%prep

%setup -q -n amanda-%{version}%{plevel}
%patch0 -p1 -b .bug18322

# re-apply this one when the patch is updated,
# there's too many rejects as is.
#%patch1 -p1 -b .append

%patch3 -p0 -b .no_private_libtool
%patch4 -p1 -b .no_uid_gid_suid_install
#%patch5 -p1 -b .dvd
%patch6 -p0 -b .perlbang
%patch7 -p0 -b .dump

# OE 20040517: fix soname
find -name "Makefile.*" | xargs perl -pi -e "s|^libamanda_la_LDFLAGS.*|libamanda_la_LDFLAGS = -version-info %{amanda_version_info}|g"
find -name "Makefile.*" | xargs perl -pi -e "s|^libamandad_la_LDFLAGS.*|libamandad_la_LDFLAGS = -version-info %{amanda_version_info}|g"
find -name "Makefile.*" | xargs perl -pi -e "s|^libamclient_la_LDFLAGS.*|libamclient_la_LDFLAGS = -version-info %{amanda_version_info}|g"
find -name "Makefile.*" | xargs perl -pi -e "s|^libamserver_la_LDFLAGS.*|libamserver_la_LDFLAGS = -version-info %{amanda_version_info}|g"
find -name "Makefile.*" | xargs perl -pi -e "s|^libamtape_la_LDFLAGS.*|libamtape_la_LDFLAGS = -version-info %{amanda_version_info}|g"
find -name "Makefile.*" | xargs perl -pi -e "s|^librestore_la_LDFLAGS.*|librestore_la_LDFLAGS = -version-info %{amanda_version_info}|g"

%build
%serverbuild

export CFLAGS="$CFLAGS -D_FILE_OFFSET_BITS=64 -D_GNU_SOURCE"
export SED=sed
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force; aclocal-1.7; automake-1.7; autoconf

%configure2_5x \
    --enable-shared \
    --with-index-server=localhost \
    --with-gnutar-listdir=%{_localstatedir}/amanda/gnutar-lists \
    --with-smbclient=%{_bindir}/smbclient \
    --with-db=text \
    --with-amandahosts \
    --with-user=amanda \
    --with-group=disk \
    --with-gnutar=/bin/tar \
    --program-transform-name="" \
    --with-ssh-security \
    --with-dumperdir=%{_libexecdir}

%make

# these won't build, why did we ship them?
#(cd common-src; make security)
#(cd tape-src; make tapetype)

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/xinetd.d
install -d %{buildroot}%{_sysconfdir}/amanda/DailySet1
install -d %{buildroot}%{_localstatedir}/amanda
install -d %{buildroot}%{_localstatedir}/amanda/gnutar-lists
install -d %{buildroot}%{_localstatedir}/amanda/DailySet1/index

%makeinstall_std BINARY_OWNER=`id -un` SETUID_GROUP=`id -gn`

bzcat %{SOURCE5} > %{buildroot}%{_sysconfdir}/xinetd.d/amanda
bzcat %{SOURCE6} > %{buildroot}%{_sysconfdir}/xinetd.d/amandaidx
bzcat %{SOURCE7} > %{buildroot}%{_sysconfdir}/xinetd.d/amidxtape
chmod 644 %{buildroot}%{_sysconfdir}/xinetd.d/*

bzcat %{SOURCE8} > %{buildroot}%{_localstatedir}/amanda/.amandahosts
chmod 660 %{buildroot}%{_localstatedir}/amanda/.amandahosts

mkdir -p examples
cp example/* examples
rm -f examples/Makefile*
rm -f examples/config.site

#cp common-src/security %{buildroot}%{_sbindir}

bzcat %{SOURCE2} > docs/__README_QUICKSETUP__
cp %{SOURCE9} docs/

{ cd %{buildroot}
  bzcat %{SOURCE1} > .%{_sysconfdir}/amanda/crontab.sample
  bzcat %{SOURCE3} > .%{_sysconfdir}/amanda/DailySet1/amanda.conf
  bzcat %{SOURCE4} > .%{_sysconfdir}/amanda/DailySet1/disklist
  touch .%{_sysconfdir}/amandates

  chmod 755 .%{_libdir}/lib* .%{_sbindir}/*
}

# remove installed docs which we let RPM handle to install
rm -rf %{buildroot}%{_datadir}/amanda

# lib64 fix
perl -pi -e "s|/usr/lib|%{_libdir}|g" %{buildroot}%{_sysconfdir}/xinetd.d/*

%pre -n %{libname}
useradd -M -n -g disk -r -d %{_localstatedir}/amanda -s /bin/bash \
	-c "system user for %{name}" amanda >/dev/null 2>&1 || :

%post client
service xinetd condrestart

%postun client
service xinetd condrestart

%post server
service xinetd condrestart

%postun server
service xinetd condrestart

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libname}-client -p /sbin/ldconfig

%postun -n %{libname}-client -p /sbin/ldconfig

%post -n %{libname}-server -p /sbin/ldconfig

%postun -n %{libname}-server -p /sbin/ldconfig

%clean 
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libamanda.so.*
%{_libdir}/libamtape.so.*
%{_libdir}/librestore.so.*
%attr(-,amanda,disk) %{_sbindir}/amrestore
%attr(600,amanda,disk)  %config(noreplace) %{_localstatedir}/amanda/.amandahosts
%attr(-,amanda,disk) %dir %{_localstatedir}/amanda/
%attr(-,amanda,disk) %dir %{_sysconfdir}/amanda/
%attr(-,amanda,disk) %config(noreplace) %{_sysconfdir}/amandates
%{_mandir}/man8/amrestore.8*
%{_mandir}/man5/amanda.conf.5*

%files server
%defattr(-,root,root)
%doc examples COPYRIGHT* NEWS README ReleaseNotes
%doc docs/*.txt
%config(noreplace) %{_sysconfdir}/xinetd.d/amandaidx
%config(noreplace) %{_sysconfdir}/xinetd.d/amidxtape
%attr(-,amanda,disk) %dir %{_libexecdir}
%attr(-,amanda,disk) %{_libexecdir}/amidxtaped
%attr(-,amanda,disk) %{_libexecdir}/amindexd
%attr(-,amanda,disk) %{_libexecdir}/amlogroll
%attr(-,amanda,disk) %{_libexecdir}/amtrmidx
%attr(-,amanda,disk) %{_libexecdir}/amtrmlog
%attr(-,amanda,disk) %{_libexecdir}/driver
%attr(4750,root,disk) %{_libexecdir}/dumper
%attr(4750,root,disk) %{_libexecdir}/planner
%attr(-,amanda,disk) %{_libexecdir}/taper
%attr(-,amanda,disk) %{_libexecdir}/amcleanupdisk
%attr(-,amanda,disk) %{_libexecdir}/chg-scsi
%attr(-,amanda,disk) %{_libexecdir}/chg-manual
%attr(-,amanda,disk) %{_libexecdir}/chg-multi
%attr(-,amanda,disk) %{_libexecdir}/chg-mtx
%attr(-,amanda,disk) %{_libexecdir}/chg-rth
%attr(-,amanda,disk) %{_libexecdir}/chg-chs
%attr(-,amanda,disk) %{_libexecdir}/chg-chio
%attr(-,amanda,disk) %{_libexecdir}/chg-zd-mtx
%attr(-,amanda,disk) %{_libexecdir}/chg-iomega
%attr(-,amanda,disk) %{_libexecdir}/chunker
%attr(-,amanda,disk) %{_libexecdir}/amcat.awk
%attr(-,amanda,disk) %{_libexecdir}/amplot.awk
%attr(-,amanda,disk) %{_libexecdir}/amplot.g
%attr(-,amanda,disk) %{_libexecdir}/amplot.gp
%attr(-,amanda,disk) %{_libexecdir}/generic-dumper
%attr(-,amanda,disk) %{_libexecdir}/gnutar
%attr(-,amanda,disk) %{_sbindir}/amadmin
%attr(4750,root,disk) %{_sbindir}/amcheck
%attr(-,amanda,disk) %{_sbindir}/amflush
%attr(-,amanda,disk) %{_sbindir}/amgetconf
%attr(-,amanda,disk) %{_sbindir}/amlabel
%attr(-,amanda,disk) %{_sbindir}/amtape
%attr(-,amanda,disk) %{_sbindir}/amreport
%attr(-,amanda,disk) %{_sbindir}/amcheckdb
%attr(-,amanda,disk) %{_sbindir}/amcleanup
%attr(-,amanda,disk) %{_sbindir}/amdump
%attr(-,amanda,disk) %{_sbindir}/amoverview
%attr(-,amanda,disk) %{_sbindir}/amrmtape
%attr(-,amanda,disk) %{_sbindir}/amtoc
%attr(-,amanda,disk) %{_sbindir}/amverify
%attr(-,amanda,disk) %{_sbindir}/amstatus
%attr(-,amanda,disk) %{_sbindir}/amplot
%attr(-,amanda,disk) %{_sbindir}/amdd
%attr(-,amanda,disk) %{_sbindir}/ammt
%attr(-,amanda,disk) %{_sbindir}/amverifyrun
%attr(-,amanda,disk) %{_sbindir}/amtapetype
%attr(-,amanda,disk) %{_sbindir}/amfetchdump
%attr(-,amanda,disk) %{_sbindir}/amcrypt-ossl
%attr(-,amanda,disk) %{_sbindir}/amcrypt-ossl-asym
%attr(-,amanda,disk) %dir %{_localstatedir}/amanda/DailySet1/
%attr(-,amanda,disk) %dir %{_localstatedir}/amanda/DailySet1/index
%attr(-,amanda,disk) %dir %{_sysconfdir}/amanda
%attr(-,amanda,disk) %dir %{_sysconfdir}/amanda/DailySet1
%attr(-,amanda,disk) %config(noreplace) %{_sysconfdir}/amanda/DailySet1/amanda.conf
%attr(-,amanda,disk) %config(noreplace) %{_sysconfdir}/amanda/crontab.sample
%attr(-,amanda,disk) %config(noreplace) %{_sysconfdir}/amanda/DailySet1/disklist

%{_mandir}/man8/amplot.8*
%{_mandir}/man8/amanda.8*
%{_mandir}/man8/amadmin.8*
%{_mandir}/man8/amcheck.8*
%{_mandir}/man8/amcheckdb.8*
%{_mandir}/man8/amcleanup.8*
%{_mandir}/man8/amdump.8*
%{_mandir}/man8/amflush.8*
%{_mandir}/man8/amlabel.8*
%{_mandir}/man8/amoverview.8*
%{_mandir}/man8/amrmtape.8*
%{_mandir}/man8/amtape.8*
%{_mandir}/man8/amtoc.8*
%{_mandir}/man8/amverify.8*
%{_mandir}/man8/amstatus.8*
%{_mandir}/man8/amreport.8*
%{_mandir}/man8/amdd.8*
%{_mandir}/man8/amgetconf.8*
%{_mandir}/man8/ammt.8*
%{_mandir}/man8/amverifyrun.8*
%{_mandir}/man8/amtapetype.8*
%{_mandir}/man8/amfetchdump.8*
%{_mandir}/man8/amcrypt-ossl-asym.8*
%{_mandir}/man8/amcrypt-ossl.8*

%files -n %{libname}-server
%defattr(-,root,root)
%{_libdir}/libamserver.so.*

%files client
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/xinetd.d/amanda
%attr(-,amanda,disk) %dir %{_libexecdir}
%attr(-,amanda,disk) %{_libexecdir}/amandad
%attr(4750,root,disk) %{_libexecdir}/calcsize
%attr(4750,root,disk) %{_libexecdir}/killpgrp
%attr(-,amanda,disk) %{_libexecdir}/patch-system
%attr(4750,root,disk) %{_libexecdir}/rundump
%attr(4750,root,disk) %{_libexecdir}/runtar
%attr(-,amanda,disk) %{_libexecdir}/selfcheck
%attr(-,amanda,disk) %{_libexecdir}/sendbackup
%attr(-,amanda,disk) %{_libexecdir}/sendsize
%attr(-,amanda,disk) %{_libexecdir}/versionsuffix
%attr(-,amanda,disk) %{_libexecdir}/chg-juke
%attr(-,amanda,disk) %{_libexecdir}/chg-rait
#%attr(-,amanda,disk) %{_libexecdir}/amqde
%attr(-,amanda,disk) %{_libexecdir}/chg-disk
%attr(-,amanda,disk) %{_libexecdir}/chg-mcutil
%attr(-,amanda,disk) %{_libexecdir}/chg-null
%attr(-,amanda,disk) %{_libexecdir}/noop
%attr(-,amanda,disk) %{_sbindir}/amaespipe
%attr(-,amanda,disk) %{_sbindir}/amcrypt
%attr(-,amanda,disk) %{_sbindir}/amrecover
%attr(-,amanda,disk) %{_sbindir}/amoldrecover

#%attr(-,amanda,disk) %{_sbindir}/security
%attr(-,amanda,disk) %{_localstatedir}/amanda/gnutar-lists/
%{_mandir}/man5/amanda-client.conf.5*
%{_mandir}/man8/amaespipe.8*
%{_mandir}/man8/amcrypt.8*
%{_mandir}/man8/amrecover.8*

%files -n %{libname}-client
%defattr(-,root,root)
%{_libdir}/libamclient.so.*
%{_libdir}/libamandad.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/lib*.so
