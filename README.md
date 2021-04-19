# Vocabulary Manager

The mission of this appilication is to provide a comprehensive platform for acquiring and retaining foreign-language vocabulary for language learners at all levels. At its core, this application is an e-book reader that is optimized for learning a new language. Users can upload documents of their choice, read them in the browser and then look up the translations of unknown words or phrases with a few simple mouse clicks. This is just the start, however. Future releases will add features for performing tasks such as acquiring vocabulary from audio sources, uploading vocabulary acquired from print media, and providing sophisticated interfaces for querying all previously-acquired vocabulary in order to build customized vocabulary-retention tests. For more on future directions, please see **vocab_manager/documentation/future/new_features.pdf**

From a more technical perspective, this application is designed to be a SaaS application. The back-end code is written in Python 3 with help from the Flask web framework. This code is used to both handle routing to different web pages as well as offer microservices that can be consumed by the front-end component of this application and by third parties. The code for the microservices can be found under **vocab_manager/app/api**.

In addition to Flask, MongoDB was used as a database for storing user data and Elasticsearch was used to provide a foreign-language dictionary service. The ETL code for populating Elasticsearch with dictionary data can be found under **vocab_manager/dictionaries**.

The front-end code is written in Javascript (ES6) with help from the React framework as well as HTML and CSS. This code allows users to upload foreign-language documents from the browser and then view them in the e-book reader. The code for the e-book reader is currently the most interesting part of the front-end code from a technical perspective and it can be found at **vocab_manager/document_viewer/document_manager**

Finally, the code for automatically scaling the Vocabulary Manager application in the cloud is written in Docker, Terraform and Ansible. The cloud provider is currently AWS. The code itself can be found at **vocab_manager/devops**