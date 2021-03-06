Title: Installing HDP 2.4.0 using Ambari 2.1
Date: 2018-03-25 11:30 PM
Modified: 2018-03-25 11:30 PM
Category: Data Analytics
Tags: HDP, vagrant, installation
Slug: hdp
Authors: Akshay Sinha
Summary: This goes through installation and setup of HDP cluster using vagrant

## Installing HDP 2.4.0 using Ambari 2.1

The other day, I was wondering if I can setup a single node hdp cluster on my laptop using vagrant. Given below are the steps to do so.

#### Prerequisite

* Vagrant
* Virtual Box
* Enough resources on host (~ 16G RAM)

#### Download Vagrant

Download and install Vagrant from [Vagrant official site](https://www.vagrantup.com/downloads.html)

#### Download Virtual Box

Download and install Virtual Box from [Virtualbox official site](https://www.virtualbox.org/wiki/Downloads)

#### Download the customized Vagrantfile and provision file from git

Credit : https://github.com/timveil/hdp-vagrant-basehttps://github.com/timveil/hdp-vagrant-base

Thanks to [Tim Veil](https://github.com/timveil) for creating a customized vagrantfile file for base install box for HDP cluster tailored to
Hortonworks install dos. Go ahead and clone the above git repository in a local directory.

I made a few changes to the above vagrant file. Overwrite the downloaded Vagrantfile with following contents. Leave the `provision-base.sh` as is :

    # -*- mode: ruby -*-
    # vi: set ft=ruby :

    Vagrant.configure("2") do |config|
        config.vm.box = "centos/7"
      config.vm.hostname = "hdp.utopia.com"

        config.vm.box_check_update = true

        config.vbguest.auto_update = false

        config.vbguest.no_remote = true

        config.vbguest.no_install = true

      config.vm.network "forwarded_port", guest: 8080, host: 8080
        config.vm.network "private_network", ip: "192.168.56.78"

        # workaround for known issue #2 https://seven.centos.org/2016/12/updated-centos-vagrant-images-available-v1611-01/
        config.vm.synced_folder ".", "/vagrant", disabled: true

        config.vm.provider "virtualbox" do |v|
            v.memory = 4096
            v.cpus = 4
        end

        config.vm.provision "base", type: "shell", path: "provision-base.sh"

    end

Note that hostname and ip can be set randomly.

#### Install Vagrant guest additions

Install Vagrant Guest additions using following command :

    vagrant plugin install vagrant-vbguest

#### Bring up Vagrant

    vagrant init timveil/centos7-hdp-base; vagrant up --provider virtualbox

Now sitback and relax, this will take some time

#### Few more Prerequisites

If all goes well, at this time, you would have a vagrant box running with all the base Prerequisite installed. Lets now ssh into the box

    vagrant ssh

Check the hostname

    hostname -f
    hostname -I

You should see `hdp.utopia.com` as the hostname and `192.168.56.78` as IP

on you host box, update `/etc/hosts`, if on linux or `C:\Windows\System32\drivers\etc\hosts`, if on windows to following :

    127.0.0.1       localhost hdp.utopia.com

This will help your host box resolve the hdp cluster host to `127.0.0.1`

Lets also generate ssh keys at this time which will be used to later for registering host with ambari.

    sudo su
    ssh-keygen
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    cat ~/.ssh/id_rsa

Make a note of contents on `id_rsa`. We will need this in future.

#### Install Ambari

At the time of writing this, Ambari 2.2.2.0 was the lastet available for HPD. Lets go ahead and add the yum repo for Ambari

    cd /tmp
    wget http://public-repo-1.hortonworks.com/ambari/centos7/2.x/updates/2.2.2.0/ambari.repo
    cp ambari.repo /etc/yum.repo.d
    yum repolist

Next, lets install Ambari

    yum install ambari-server

Once ambari-server is installed, we need to configure it

    ambari-server setup

I choose to go ahead with default configurations. You can choose as required.

Once the setup is done, start ambari-server

    ambari-server start

Now from command line, try following curl :

    curl -k http://hpd.utopia.com:8080/

This should come back with and html response. If it does, the installation was successful. Lets go ahead and try that out from our host's browser. Default username and password are `admin`

* Click on `Install Cluster Wizard` and provide a cluster hostname.
* On the next page, we will need to register the hosts with ambari. Start by inpuring the hostname `hdp.utopia.com` in the hostname field. Remember how we copied the contents of `id_rsa` earliar. That needs to be entered into `ssh public key` text box. Thats it, click next.

Ambari will now register your host. This might take some time. You can tail the logs at `/var/log/ambari-server/ambari-server.log`.

Once the host is registered, go ahead and choose that components that you need to install, review them and deploy. That's it !!

#### Troubleshooting

##### javax.net.ssl.SSLException: Received fatal alert: unknown_ca

In my case `registring hosts` steps was failing repeatedly with following error :

    javax.net.ssl.SSLException: Received fatal alert: unknown_ca

The error could be seen in `/var/log/ambari-server/ambari-server.log` logs. In order to resolve that, I had to disable the cert verification in `/etc/python/cert-verification.cfg` file :

    # Possible values are:
    # 'enable' to ensure HTTPS certificate verification is enabled by default
    # 'disable' to ensure HTTPS certificate verification is disabled by default
    # 'platform_default' to delegate the decision to the redistributor providing this particular Python version

    # For more info refer to https://www.python.org/dev/peps/pep-0493/
    [https]
    verify=disable

by default, `verify` is set to `platform_default`
