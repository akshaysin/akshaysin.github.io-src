Title: Linux Hacks
Date: 2018-4-29 17:27
Modified: 2018-4-29 17:27
Category: Linux Hacks
Tags: linux
Slug: linux-hacks
Authors: Akshay Sinha
Summary: Linux Hacks for day to day

## Linux Hacks

Here is a goto list of linux hacks that I find useful in my day to day. I will keep on updating it as I gather more. Please feel free to respond back in comments in case you want me to add some more

### Random Password Generator

Following two scripts generate a random string, a sub set of which, or the whole string can be used as an password. Give it a try.

```date +%s | sha256sum | base64 | head -c 32 ; echo
< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-32};echo;
```

### Removing trailing spaces

    echo "   lol  " | xargs

Xargs will do the trimming for you. It's one command/program, no parameters, returns the trimmed string, as easy as that!
Note: this doesn't remove the internal spaces so "foo bar" stays the same. It does NOT become "foobar".

### Breaking a file into smaller chunks

    # By Size
    split -b 100M -d -a 3 forever.log.bck forever

    # By number of Lines (input and output are just two directories)
    split -l 2500 input/result.txt output/result.txt

### Search and replace a string in all files in my present directory

    sed -i -- 's/STR1/STR2/g' *

This replaces all occurances of _STR1_ with _STR2_ in all files in my current directory

### Delete logs older than X days

    find /path/to/files* -mtime +X -exec rm {} \;

### Total number of lines in all the files in current directory

    find . -type f -exec cat {} + | wc -l  

### Install FTP on rhel or centos

    yum install vsftpd -y
    yum install ftp -y
    service vsftpd start

### Install jq

[jq](https://stedolan.github.io/jq/) is a really cool tool if you work with json's a lot. Its like sed for json. You can use it to slice and filter and map and transform structured data with the same ease that sed, awk, grep and friends let you play with text.

Installing it is an breeze too

    wget -O jq https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64
    chmod +x ./jq
    cp jq /usr/bin
    rm jq

### Using tcpdump

Although a whole seperate blog could be ritten about tcpdump and its usage. Here is a very short, quick and dirty SOP to get it up and running
Please note that sudo access is required for this

    # Install tcpdump
    yum install tcpdump

    # Use tcpdump to capture network traffic and write a Wireshark-compatible pcap file:
    tcpdump -s 0 port 443 -w mypcapfile.pcap

    # Terminate the capture with a ctl-c

    # gzip the file:
    gzip mypcapfile.pcap
