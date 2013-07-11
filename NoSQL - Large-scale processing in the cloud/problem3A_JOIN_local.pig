-- In this problem we will consider the subgraph consisting of triples whose subject matches rdfabout.com: for that, filter on subject matches '.*rdfabout\\.com.*'. Find all chains of lengths 2 in this subgraph. More precisely, return all sextuples (subject, predicate, object, subject2, predicate2, object2) where object=subject2.


-- for local mode
register myudfs.jar

-- load the test file into Pig in LOCAL
 raw = LOAD 'source_code/cse344-test-file' USING TextLoader as (line:chararray);

-- parse each line into ntriples
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject1:chararray,predicate1:chararray,object1:chararray);

-- filter by subject matches '.*business.*'
A = FILTER ntriples BY subject1 matches '.*business.*';

-- copy A in B and rename
B = foreach A generate subject1 as subject2, predicate1 as predicate2, object1 as object2;

-- make the JOIN
C = JOIN A BY subject1, B BY subject2;

-- count how many
c1 = group C all;
counter = foreach c1 generate COUNT(C) PARALLEL 50;
