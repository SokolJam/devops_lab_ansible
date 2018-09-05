# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure("2") do |config|
   config.vm.box = "sbeliakou/centos"
   config.vm.box_version = "7.5"

   config.vm.define "web" do |webserver|
   webserver.vm.provider "virtualbox" do |wserver|
    wserver.name = "webserver"
    wserver.memory = "1024"
   end
   webserver.vm.hostname = "httpd"
   webserver.vm.network "private_network", ip: "192.168.10.2"
  end

   config.vm.define "app" do |appserver|
    appserver.vm.provider "virtualbox"  do |aserver|
     aserver.name = "appserver"
     aserver.memory = "2048"
    end
    appserver.vm.hostname = "jenkins"
    appserver.vm.network "private_network", ip: "192.168.10.3"
   end
  
end
