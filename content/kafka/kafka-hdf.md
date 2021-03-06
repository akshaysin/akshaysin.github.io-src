Title: Kafka Messaging Infrastructure installation using HDF
Date: 2018-04-11 10:00 PM
Modified: 2018-04-11 10:00 PM
Category: Various
Tags: kafka, zookeeper, installation
Slug: hdf-kafka
Authors: Akshay Sinha
Summary: Kafka Messaging Infrastructure installation using HDF

## Kafka Messaging Infrastructure installation using HDF.

Although kafka/zookeeper can of course be installed as an standalone service, I have found leveraging hortonworks hdf, a more tailored approach of setting it up. HDF already comes with a set of tools in addition to kafka and zookeeper, which can be utilized to extend the features of cluster in future if needed.

### Prerequisites

* 4 Boxes, one to be used as Ambari node and others as kafka nodes
* Sudo access on all boxes
* HDF 3.1, at the time of writing. Make sure to use the most latest one from : https://docs.hortonworks.com/HDPDocuments/HDF3/HDF-3.1.1/index.html

### Steps to be performed on all four boxes

Create a user `amusr` on all nodes and make sure it has password less sudo rights `amusr ALL=(ALL) NOPASSWD: ALL`
On all the nodes, install nscd `sudo yum -y install nscd && sudo setenforce 0 && sudo yum install -y wget`
Login to future Ambari management host as `amusr` and follow following commands

    cd ~ && ssh-keygen (accept all the defaults)


Copy amusr public key from ambari-server host to all target hosts. Remember if you plan to use ambari server too as one of the kafka node, make to execute below commands on ambari-server too.

    copy ~/.ssh/id_rsa.pub to `amusr` home directory on all target hosts
    Add the SSH Public Key to the authorized_keys file on your target hosts. `cat id_rsa.pub >> ~/.ssh/authorized_keys`
    chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys


From the Ambari Server, make sure you can connect to each host in the cluster using SSH, without having to enter a password. `ssh amusr@<remote.target.host>`

### Install Ambari

    wget -nv http://public-repo-1.hortonworks.com/ambari/centos7/2.x/updates/2.6.1.0/ambari.repo -O /etc/yum.repos.d/ambari.repo
    sudo yum repolist
    sudo yum -y install ambari-server
    sudo ambari-server setup
    sudo ambari-server start
    sudo ambari-server status


### Setup HDF local repository on ambari node

Depending on what is the latest version of hdf available at that time, update the below commands based on that. You should be able to reference the current release notes of the latest version to get the repo endpoint

Ref : https://docs.hortonworks.com/HDPDocuments/HDF3/HDF-3.1.1/bk_release-notes/content/ch_hdf_relnotes.html#repo-location

    sudo wget -nv http://public-repo-1.hortonworks.com/HDF/centos7/3.x/updates/3.1.1.0/hdf.repo -O /etc/yum.repos.d/hdf.repo
    cd /tmp && sudo wget http://public-repo-1.hortonworks.com/HDF/centos7/3.x/updates/3.1.1.0/tars/hdf_ambari_mp/hdf-ambari-mpack-3.1.1.0-35.tar.gz
    sudo ambari-server install-mpack --mpack=/tmp/hdf-ambari-mpack-3.1.1.0-35.tar.gz --purge --verbose
    sudo ambari-server stop
    sudo ambari-server start

This completes the installation of ambari-server. Rest of the installation will proceed from UI

### Using Ambari to install HDFS
If all goes well, at this time, you should be able to get to access ambari over browser:

  * Goto http://ambariserver:8080 and enter username and password as `admin/admin`
  * Launch Install Wizard
  * Name the cluster like kafka_envname
  * Select Most latest Version and repository
  * Add Fully qualified hostnames and content of amusr's private key in the UI. Also make sure to change the username from `root` to `amusr`. Click Next
  * Once registration succeeds, choose below services :
      * Zookeeper
      * Ambari Infra
      * Ambari Metrics
      * Kafka
      * Log Search
  * Select Master nodes and slave nodes as follows :

      |Hosts	       |  Services                                                       |
      |------------- | ----------------------------------------------------------------|
      |ambari-server |  Infra Solr Instance,Grafana,Metrics Collector,Log Search Server|
      |kafka-node1	 |  ZooKeeper Server,Kafka Broker|
      |kafka-node2	 |  ZooKeeper Server,Kafka Broker|
      |kafka-node3	 |  ZooKeeper Server,Kafka Broker|

  * Review and confirm

### Security
Kafka ships with an out of box authorizer. What that means is that it gives you the ability to setup acls across topics and restrict them to the users you like. I have found client cert mutual authentication coupled with this acl approach to be very effective. Please refer to folowing two bolgs for more details :

  * [Setting up Client cert mutual authentication in a kafka hdf cluster]({filename}/kafka/2018_06_09_kafka_ssl.md)
  * [Authorization setup in Ambari Kafka based on ACLs]({filename}/kafka/2018_06_09_kafka_acls.md)
