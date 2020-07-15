# BEng-Thesis---Semantic-Analysis

Links:

https://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html - RDFlib documentation    
https://metamap.nlm.nih.gov/ - MetaMap    
https://github.com/AnthonyMRios/pymetamap - Python MetaMap Wrapper   
https://www.analyticsvidhya.com/blog/2019/02/stanfordnlp-nlp-library-python/   

Google docs:  
https://docs.google.com/document/d/1_QnFcBCXC_uLj0TBx6UYta7S3KJnFscf8mVn6Dcl9OE/edit?fbclid=IwAR3m4udPSerpgEE3DNBL4vVQ502eXzsFg2XuXpb1JWNVlX0lRrTfR4Gpfiw

Server setup:   
* Download the CoreNLP package. Open your Linux terminal and type the following command:

`wget http://nlp.stanford.edu/software/stanford-corenlp-full-2020-04-20.zip`
* Unzip the downloaded package:

`unzip stanford-corenlp-full-2020-04-20.zip`
* Start the CoreNLP server:

`java -mx8g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000`

Enviromental variables setup:
* You need to set `CORENLP_HOME` variable.   
Linux/MacOS: Add `export CORENLP_HOME=<path-to-unzipped-folder>/stanford-corenlp-full-2020-04-20` 
to `~\.bash_profile` or `etc\.profile` or `~\.zhrc` and run `source ~\.zhrc` (or the file of choice) in the console.  
Windows: Add `CORENLP_HOME=<path-to-unzipped-folder>/stanford-corenlp-full-2020-04-20` to System Enviromental Variables.

MetaMap Wrapper instalation guide - https://metamap.nlm.nih.gov/Installation.shtml

The 'public_mm' folder needs to be in the root directory of the project.

