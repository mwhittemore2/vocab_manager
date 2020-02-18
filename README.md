# Vocabulary Manager

This application is designed to integrate the foreign language vocabularies a user acquires from both electronic sources (like websites and text files) and paper sources (like books and magazines). While there are technologies that already exist to acquire vocabulary words electronically, they don't easily support tracking vocabulary words that can be acquired from offline sources. As a foreign language learner, the lack of such tools enabling vocabulary consolidation across multiple media was a source of difficulty for me for years, which is why I undertook this project.

To reach the goal of offering a consolidated vocabulary management tool, the project currently supports the following web services:

    -- Addition and deletion of acquired foreign language vocabulary along with their context

    -- Dictionary translations from German to English (more languages to come)
    
    -- Access to foreign language resources a user has acquired

These services can be found under vocab_manager/app/api. From a technical perspective, the back-end code for these services is written in Python with Flask used as the web framework for supporting these services. In addition, MongoDB was used as a database for storing user data
and Elasticsearch was used to provide a foreign language dictionary service. The code for populating Elasticsearch with dictionary data can be found under vocab_manager/dictionaries.

The front-end component of the project should be regarded only as a skeleton, but I plan to eventually build it out using React.

The project is still ongoing. More features to support management of non-electronic vocabulary sources are planned for future releases. Please keep checking for further updates.
