python mrjob_crash_counts.py \
       -r emr s3://your-bucket-name-here/ \
       --output-dir=s3://your-bucket-name-here/crash-counts 
       --conf-path=</path/to/your/config/file.conf>
