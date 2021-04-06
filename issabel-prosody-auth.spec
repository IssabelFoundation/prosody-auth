%define modname prosody-auth

Summary: This package is used for issabel-prosody-auth
Name: issabel-prosody-auth
Version: 1.0
Release: 2
License: GPL
Source0: issabel-%{modname}-%{version}.tar.gz
Group: System/Administration
Vendor: Issabel Foundation
Packager: info@issabel.org
BuildArch: noarch

AutoReqProv: no
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Requires: lua
Requires: prosody
Requires: perl-Unix-Syslog
Requires: perl-Switch
Requires: perl-Text-Iconv
Requires: perl-DBD-SQLite

%description 
Package issabel-prosody-auth

%prep
#%setup -q 
#-n %{name}-%{version}
%setup -c -q

%build

%install
rm -Rf %{buildroot}
#mkdir -p %{buildroot}/usr/lib/debug
mkdir -p %{buildroot}/usr/share/issabel/privileged
mkdir -p %{buildroot}/usr/lib64/prosody/modules/mod_auth_external
mkdir -p %{buildroot}/etc/prosody/conf.d

#Files installation
[ -d "`dirname %{buildroot}/mod_auth_external.lua`" ] || %{__mkdir_p} "`dirname %{buildroot}/mod_auth_external.lua`"
%{__install} -m 0644 "issabel-%{modname}-%{version}/setup/usr/lib64/prosody/modules/mod_auth_external/mod_auth_external.lua" "%{buildroot}/usr/lib64/prosody/modules/mod_auth_external/mod_auth_external.lua"
[ -d "`dirname %{buildroot}/issabelprosody.pl`" ] || %{__mkdir_p} "`dirname %{buildroot}/issabelprosody.pl`"
%{__install} -m 0755 "issabel-%{modname}-%{version}/setup/usr/lib64/prosody/modules/mod_auth_external/issabelprosody.pl" "%{buildroot}/usr/lib64/prosody/modules/mod_auth_external/issabelprosody.pl"

%{__install} -m 0755 "issabel-%{modname}-%{version}/setup/usr/share/issabel/privileged/prosodygroup" "%{buildroot}/usr/share/issabel/privileged/prosodygroup"

[ -d "`dirname %{buildroot}/auth.cfg.lua`" ] || %{__mkdir_p} "`dirname %{buildroot}/auth.cfg.lua`"
%{__install} -m 0644 "issabel-%{modname}-%{version}/setup/etc/prosody/conf.d/auth.cfg.lua" "%{buildroot}/etc/prosody/conf.d/auth.cfg.lua"
[ -d "`dirname %{buildroot}/groups.cfg.lua`" ] || %{__mkdir_p} "`dirname %{buildroot}/groups.cfg.lua`"
%{__install} -m 0644 "issabel-%{modname}-%{version}/setup/etc/prosody/conf.d/groups.cfg.lua" "%{buildroot}/etc/prosody/conf.d/groups.cfg.lua"
[ -d "`dirname %{buildroot}/issabel.cfg.lua`" ] || %{__mkdir_p} "`dirname %{buildroot}/issabel.cfg.lua`"
%{__install} -m 0644 "issabel-%{modname}-%{version}/setup/etc/prosody/conf.d/issabel.cfg.lua" "%{buildroot}/etc/prosody/conf.d/issabel.cfg.lua"
[ -d "`dirname %{buildroot}/sharedgroups.txt`" ] || %{__mkdir_p} "`dirname %{buildroot}/sharedgroups.txt`"
%{__install} -m 0644 "issabel-%{modname}-%{version}/setup/etc/prosody/sharedgroups.txt" "%{buildroot}/etc/prosody/sharedgroups.txt"
[ -d "`dirname %{buildroot}/updategroup.sh`" ] || %{__mkdir_p} "`dirname %{buildroot}/updategroup.sh`"
%{__install} -m 0755 "issabel-%{modname}-%{version}/setup/etc/prosody/updategroup.sh" "%{buildroot}/etc/prosody/updategroup.sh"
[ -d "`dirname %{buildroot}/runprosodycmd`" ] || %{__mkdir_p} "`dirname %{buildroot}/runprosodycmd`"
%{__install} -m 0755 "issabel-%{modname}-%{version}/setup/etc/prosody/runprosodycmd" "%{buildroot}/etc/prosody/runprosodycmd"

%pre
# No group Creation
# No User Creation


%post

if [ -f /etc/prosody/prosody.cfg.lua ]; then
    sed -i 's/^authentication = /-- authentication = /g' /etc/prosody/prosody.cfg.lua
    sed -i 's/--"groups"/"groups"/g' /etc/prosody/prosody.cfg.lua
    sed -i 's/--"admin_telnet"/"admin_telnet"/g' /etc/prosody/prosody.cfg.lua
    /etc/prosody/updategroup.sh
fi

if [ ! -f /etc/pki/prosody/issabel.crt ]; then
    cd /etc/pki/prosody
    make issabel.cnf
    make issabel.key
    make issabel.crt
    chgrp prosody /etc/pki/prosody/issabel*
    chmod g+r /etc/pki/prosody/issabel*
fi

%preun

%postun

%clean
rm -Rf %{buildroot}

#Regular file and dir list
%files
%attr(0644 root, root) "/usr/lib64/prosody/modules/mod_auth_external/mod_auth_external.lua"
%attr(0755 root, root) "/usr/lib64/prosody/modules/mod_auth_external/issabelprosody.pl"
%attr(0644 root, root) "/etc/prosody/conf.d/auth.cfg.lua"
%attr(0644 root, root) "/etc/prosody/conf.d/groups.cfg.lua"
%attr(0644 root, root) "/etc/prosody/conf.d/issabel.cfg.lua"
%attr(0644 root, root) "/etc/prosody/sharedgroups.txt"
%attr(0755 root, root) "/etc/prosody/updategroup.sh"
%attr(0755 root, root) "/etc/prosody/runprosodycmd"
%attr(0755 root, root) "/usr/share/issabel/privileged/prosodygroup"

%changelog
