Vagrant.configure("2") do |config|

  config.vm.box = "auto-google-search-centos64"

  config.vm.box_url = "http://developer.nrel.gov/downloads/vagrant-boxes/CentOS-6.4-x86_64-v20130427.box"

  config.vm.network :private_network, ip: "192.168.19.19"
  config.vm.synced_folder "puppet-configurations/", "/usr/share/puppet/"
  config.vm.synced_folder ".", "/vagrant", :mount_options => ['dmode=755,fmode=755']

  config.vm.hostname = "autogooglesearch.local"

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet-configurations"
    puppet.manifest_file  = "puppet-manifest.pp"
  end
end
