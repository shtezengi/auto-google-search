class packages {

    package { 'ftp':
        ensure => 'present',
        name => 'ftp',
    }

    package { 'ctags':
        ensure => 'present',
        name => 'ctags',
    }

    package { 'git':
        ensure => 'present',
        name => 'git',
    }

    package { "wget":
        ensure => present,
    }
}


class services {

    exec { "mysqld-service-restart":
        command => '/sbin/service mysqld restart; exit 0';
    }

    service { "iptables":
        ensure => stopped,
        enable => false,
    }

    exec { "python27-enable":
        require => Package["python27-python"],
        unless => "grep 'scl enable python27' ~$unix_user/.bash_profile 2>/dev/null",
        command => "echo 'exec scl enable python27 bash' >> ~$unix_user/.bash_profile",
        user => "vagrant",
        path => ["/bin", "/usr/bin", "/usr/local/bin"],
    }

    exec { "timezone-adjustment":
        command => "sudo mv /etc/localtime /etc/localtime.bak; sudo ln -s /usr/share/zoneinfo/America/Los_Angeles /etc/localtime;",
        user => "vagrant",
        path => ["/bin", "/usr/bin", "/usr/local/bin"],
        creates => '/etc/timezone-adjusted',
    }
}


class synceddirs {

    $synceddirs = ['/var/www/' ,
               '/var/www/auto-google-search/',
               '/var/log/django']

    file { $synceddirs :
        ensure => 'directory',
        mode => 755,
    }

}


class mysqld {

    package { 'mysql-server':
        ensure => installed,
    }

    service { "mysqld":
        ensure		=> running,
        enable 		=> true,
        name		=> "mysqld",
        hasrestart 	=> true,
        hasstatus 	=> true,
    }

    Package['mysql-server'] ->
    Service['mysqld']
}


class httpd {

    package { 'httpd':
        ensure => installed,
    }

    package { 'curl':
        ensure => "present",
    }

    service { "httpd":
        ensure => running,
        enable => true,
        name => "httpd",
        hasrestart => true,
        hasstatus => true,
    }

    Package['httpd'] ->
    Package['curl'] ->
    Service['httpd']
}


class python {
    yumrepo { "scl_python27":
        descr => "Python 2.7 Dynamic Software Collection",
        baseurl => "http://people.redhat.com/bkabrda/python27-rhel-6/",
        failovermethod => "priority",
        enabled => 1,
        gpgcheck => 0,
        http_caching => all,
    }
    package { "python27-python":
        ensure => present,
        require => Yumrepo["scl_python27"],
    }
    package { "python27-python-devel":
        ensure => present,
        require => Yumrepo["scl_python27"],
    }
    package { "python27-python-setuptools":
        ensure => present,
        require => Yumrepo["scl_python27"],
    }
    package { "python27-python-virtualenv":
        ensure => present,
        require => Yumrepo["scl_python27"],
    }
    package { "libjpeg-turbo-devel":
        ensure => present,
        require => Yumrepo["scl_python27"],
    }
    package { "libzip-devel":
        ensure => present,
        require => Yumrepo["scl_python27"],
    }
    package { "libtiff-devel":
        ensure => present,
        require => Yumrepo["scl_python27"],
    }
    package { "freetype-devel":
        ensure => present,
        require => Yumrepo["scl_python27"],
    }
    package { "tcl-devel":
        ensure => present,
        require => Yumrepo["scl_python27"],
    }
    package { "tk-devel":
        ensure => present,
        require => Yumrepo["scl_python27"],
    }
    package { "mysql":
        ensure => present,
    }
    package { "mysql-devel":
        ensure => present,
    }
}


class databasesetup {
  exec { 'auto-google-search-database-user':
        command => 'chmod +x /usr/share/puppet/files/auto-google-search-database-user.sh; /usr/share/puppet/files/auto-google-search-database-user.sh',
        path => [
            '/usr/bin',
            '/bin',
            '/sbin',
            '/usr/sbin',
            '/usr/local/bin',
        ],
        creates		=> '/root/db.auto-google-search.user',
        logoutput	=> true,
        user		=> 'root',
    }
}


include packages
include synceddirs
include mysqld
include httpd
include python
include services
include databasesetup


Class['packages'] ->
Class['synceddirs'] ->
Class['mysqld'] ->
Class['httpd'] ->
Class['python'] ->
Class['services'] ->
Class['databasesetup']
