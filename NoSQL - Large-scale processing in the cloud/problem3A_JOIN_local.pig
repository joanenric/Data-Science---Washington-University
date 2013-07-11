-- for AWS
-- register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- for local mode
register myudfs.jar

-- load the test file into Pig in LOCAL
 raw = LOAD 'source_code/cse344-test-file' USING TextLoader as (line:chararray);

-- load the test file into Pig in AWS
-- raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray); 
-- later you will load to other files, example:
-- raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray);


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

-- store the results in the folder /user/hadoop/example-results
-- store counter into '/user/hadoop/example-result1' using PigStorage();

