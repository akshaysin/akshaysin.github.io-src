Title: Automated Release Management for cloudant design documents
Date: 2018-7-18 20:42
Modified: 2018-7-18 20:42
Category: Python
Tags: Python, Cloudant, Couchdb
Slug: designdocs_automated
Authors: Akshay Sinha
Summary: Automated Release Management for cloudant design documents
status: draft

## Automated Release Management for Cloudant design documents

A bit of history about Cloudant, couchdb and thr role of design documents first. That should give us enough context to understand why was this automated proccess needed in first place.

**Systems Involved**

* Nodejs loopback
* Cloudant

**Background**

Historically, the way nosql databases chose to expose their data was, only an indexed field in an database could be used to query data from that database. The `id` field by default is always indexed. The way this works in the background is that cloudant would then use binary tree data structures to store all that data on file system by that field. Now this works great if :

* you don't have a lot of fields,
* or you don't chose to index all_fields,
* or your databases are not too big.

None of the above applied to us. We had :

* A lot of fields per document. But as would any elaborate implementation would end up having many fields overtime, so did ours.
* What we found was that loopback-cloudant-connector by default imposes a little hack of its own that it will create an `all_fields` index on all the databases that its used with. This might sound harmless at first but imagine having databases the size of 100 Million docs and applying this index on that database. The indexing job on that cluster itself would use up all resources.
* All the databases that we worked with were big to huge in size.

We eneded up opening a ticket with loopback cloudant connector support group to suppress this `all_fields` behaviour on their end. And they did. [Here](https://github.com/strongloop/loopback-connector-cloudant/issues/162) is the link to that discussion.

On our end, we decided to only create custom indexes for the fields that were indeed needed by application at run time. Now I am talking about some 50 databases, on average 4 index documents per database, spread across 14 cloudant instances. Moreover since each each enviornment was in a different stage of development, they might have different versions of the index document in each env. Logistically deploying and maintaining this manually would have been an nightmare. 
