#!/usr/bin/perl
my $dbName="/var/www/db/acl.db";
my $dbTable="acl_user";
my $fieldUser="name"; 
my $fieldPass="md5_password";

#===================================================
use Unix::Syslog qw(:macros :subs);
use Switch;
use DBI;
use Digest::MD5 qw(md5 md5_hex md5_base64);
use Text::Iconv;

my $conv_1251_utf = Text::Iconv->new("cp1251", "utf8");
my $conv_koi8_utf = Text::Iconv->new("koi8-r", "utf8");

while ( chomp ( $_ = <STDIN>) and length $_){

    my ($op,$user,$domain,$password) = split /:/,$_;
    
    # Filter dangerous characters
    $user     =~ s/[."\n\r'\$`]//g;
    $password =~ s/[."\n\r'\$`]//g;

    my $pass1251 = $conv_1251_utf->convert($password);
    my $passkoi8 = $conv_koi8_utf->convert($password);

    $md5pass0 = md5_hex($password);
    $md5pass1 = md5_hex($pass1251);
    $md5pass2 = md5_hex($passkoi8);
    $md5pass3 = $password;

    my $result;
    my $dbh = DBI->connect("DBI:SQLite:$dbName", '', '') || die "Could not connect to database: $DBI::errstr";
    switch ($op) {
        case "auth" {
            my $query="SELECT COUNT(*) FROM $dbTable WHERE $fieldUser='$user' AND ($fieldPass='$md5pass0' OR $fieldPass='$md5pass1' OR $fieldPass='$md5pass2' OR $fieldPass='$md5pass3');";
            #syslog LOG_INFO, sprintf("query: %s", $query);
            my $sth = $dbh->prepare($query);
            $sth->execute();
            @result = $sth->fetchrow_array();
            syslog LOG_INFO, "$user auth result: $result[0]";
        }
        case "isuser" {
            my $query="SELECT COUNT(*) FROM $dbTable WHERE $fieldUser='$user';";
            #syslog LOG_INFO, sprintf("query: %s", $query);
            my $sth = $dbh->prepare($query);
            $sth->execute();
            @result = $sth->fetchrow_array();
            syslog LOG_INFO, "$user existence result: $result[0]";
        }
        case default {
            $result=0;
        }
    }
    my $out = $result[0]?1:0;
    print "$out\n";
}
closelog;
