-- for AWS
register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig in LOCAL
-- raw = LOAD 'source_code/cse344-test-file' USING TextLoader as (line:chararray);

-- load the test file into Pig in AWS
-- raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray); 
-- later you will load to other files, example:
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-*' USING TextLoader as (line:chararray);

-- parse each line into ntriples
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);

--group the n-triples by subject column
subjects = group ntriples by (subject) PARALLEL 50;

-- flatten the objects out (because group by produces a tuple of each object
-- in the first column, and we want each object ot be a string, not a tuple),
-- and count the number of tuples associated with each object
count_by_object = foreach subjects generate flatten($0), COUNT($1) as count PARALLEL 50;


--order the resulting tuples by their count in descending order
count_by_object_ordered = order count_by_object by (count)  PARALLEL 50;

-- group by counter
occurr_by_count = group count_by_object_ordered by (count) PARALLEL 50;

-- count the occurrences

points = foreach occurr_by_count generate flatten($0), COUNT($1) as y PARALLEL 50;

-- b = group points all;
-- number_of_points = foreach b generate COUNT(points);

-- store the results in the folder /user/hadoop/example-results
store points into '/user/hadoop/example-result1' using PigStorage();
-- store number_of_points into '/user/hadoop/example-result2' using PigStorage();
-- store in local
-- store points into 'results/problem2A' using PigStorage();
-- fs -getmerge results/problem2A results/problem2A.txt

-- Alternatively, you can store the results in S3, see instructions:
