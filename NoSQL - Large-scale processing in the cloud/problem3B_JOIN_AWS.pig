
--In this problem we will consider the subgraph consisting of triples whose subject matches rdfabout.com: for that, filter on subject matches '.*rdfabout\\.com.*'. Find all chains of lengths 2 in this subgraph. More precisely, return all sextuples (subject, predicate, object, subject2, predicate2, object2) where object=subject2.





-- for AWS
 register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig in AWS
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray);


-- parse each line into ntriples
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject1:chararray,predicate1:chararray,object1:chararray);

-- filter by subject matches '.*rdfabout\\.com.*'
A = FILTER ntriples BY subject1 matches '.*rdfabout\\.com.*';

-- copy A in B and rename
B = foreach A generate subject1 as subject2, predicate1 as predicate2, object1 as object2;

-- make the JOIN
C = JOIN A BY object1, B BY subject2;

C = DISTINCT C;

store C into '/user/hadoop/example-result1' using PigStorage();

