Title: Installing and getting started with Rundeck
Date: 2018-03-18 11:30 AM
Modified: 2018-03-18 11:30 AM
Category: Devops
Tags: Rundeck, installation
Slug: rndeck
Authors: Akshay Sinha
Summary: This goes through installation and setup of rundeck

### Server Installation

I tested this out on a RHEL. Other meathods are available @http://rundeck.org/2.8.4/administration/installation.html

    rpm -Uvh http://repo.rundeck.org/latest.rpm
    yum install rundeck
    service rundeckd start

or get the binary from https://bintray.com/rundeck/rundeck-rpm and then do a yum install

At this time rundeck should be running at http://SERVERNAME:4440/menu/home

Thats it, Login to dashboard using admin/admin

### Start/Stop/Restart

    service rundeckd start
    service rundeckd stop
    service rundeckd restart

### Issues after installation

After initial installtion, I noticed that rundeck still defaults to localhost few times, it that happens, apply this fix

Update ```/etc/rundeck/rundeck-config.properties``` and ```/etc/rundeck/framework.properties``` to replace "localhost" to actual hostname. Also in ```/etc/rundeck/rundeck-config.properties```, change ```"grails.serverURL=http://localhost:4440"```

This is how they should look like after making the change

framework.properties

    framework.server.name = SERVERNAME
    framework.server.hostname = SERVERNAME
    framework.server.url = http://SERVERNAME:4440

rundeck-config.properties

    grails.serverURL=http://SERVERNAME:4440

After this restart the services. Note that I had to kill -9 the services for this to take effect

### rundeck cli installtion

Sometimes you would wanna use rundeck commandline for most common of tasks. For this do a yum install as below

    yum install rundeck-cli.noarch

and add following to ```~/.bash_profile``` (if the installation was done as root, make sure to switch to rundeck at this time)

    export RD_URL=http://SERVERNAME:4440
    export RD_USER=admin
    export RD_PASSWORD=admin

Finally source your profile

    . ~/.bash_profile

## Common Configurations

**Any configurations from here onwards should be done using ```rundeck``` user unless explicitly specified.

### Create Project

    su - rundeck
    rd projects create -p utopia

### Defining Nodes :

create following file /var/rundeck/projects/utopia/nodes/resources.xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project>
      <node name="web01" description="web01" tags="web"
        hostname="utopia1.lets.try.com" username="testusr"
        osFamily="unix" osName="Linux">
        <attribute name="proxy" value="utopia-qa.lets.try.com"/>
      </node>
      <node name="db01" description="db01" tags="db"
        hostname="utopia2.lets.try.com" username="testusr"
        osFamily="unix" osName="Linux">
        <attribute name="proxy" value="utopia-qa.lets.try.com"/>
      </node>
    </project>

### Defining model :

Now that nodes are defined, we need to make rundeck aware of what new hosts are there, define the model

open ```/var/rundeck/projects/utopia/etc/project.properties``` and add following two lines to end of that file :

     resources.source.2.config.directory=/var/rundeck/projects/utopia/nodes
     resources.source.2.type=directory

This way we define a new resource source for rundeck to look from

## Using rundeck in ssh-password authentication mode

By default Rundeck works with ssh keys, however if you wish to use password authentication as your preffered way of authentication, you will need to configure rundeck to do so. To achive this, a couple of configurations have to be made :

    - Enable SSH Password Authentication at either global, project or node level
    - Upload password as a key to rundeck

### Enabling SSH Password Authentication at rundeck global level

**If the rundeck installation was done using ```root```, this step should be executed using ```root```

Add follwoing line to ```/etc/rundeck/framework.properties``` to enable password authentication by default

    framework.ssh-authentication=password

If you wish to keep this setting at project level, update ```project.properties``` using the below settings

    project.ssh-authentication=password

### Adding password key to rundeck

Goto ```Settings (top right) --> Key Storage --> Add or Upload a Key```
Select ```Key Type``` as ```Password```, enter password as text, put ```Storage path``` appropriately, assign a name and click save

Next add following line to project.properties :

    project.ssh-password-storage-path=keys/utopia/rundeck.passwd
