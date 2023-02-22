# pdf-textbook-extractor


PDF Data Extractor for sejarah textbooks

 - current data collected - form 1,2,3,5 sejarah
 
Using the page number obtained from isi kandungan pages, extract the content of the pages by topic and chapter

flow:
read data source > extract isi kandungan page for (chapter, topic, page_num) > extract content from specific pages


Output file : 
isi_sejarahf[x].xlsx - large chunk
sejarah_f[x].xlsx - small chunk
