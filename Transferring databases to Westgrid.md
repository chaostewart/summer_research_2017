1. Use mysqldump to dump MySQL databse from server to local home directory, save as file `dbdump.sql`.

        cs-cl-03:~% mysqldump -hcs-oschulte-01.cs.sfu.ca -uroot -p******** DATABASE_NAME > dbdump.sql

2. Transfer `dbdump.sql` to /global/scratch/functor using scp. 

        cs-cl-03:~% scp
        usage: scp [-12346BCpqrv] [-c cipher] [-F ssh_config] [-i identity_file]
                  [-l limit] [-o ssh_option] [-P port] [-S program]
                  [[user@]host1:]file1 ... [[user@]host2:]file2
        cs-cl-03:~% scp ~/dbdump.sql functor@bugaboo.westgrid.ca:/global/scratch/functor/
        functor@bugaboo.westgrid.ca's password: ********
        dbdump.sql                                    100%  820KB 820.4KB/s   00:01    
        
3. Start an ssh session on functor account under bugaboo 

        cs-cl-03:~% ssh functor@bugaboo.westgrid.ca
        functor@bugaboo.westgrid.ca's password: ********
        Last login: Wed Jun 21 10:57:24 2017 from cs-cl-03.cs.sfu.ca
        functor@bugaboo:~>        

4. Run `./fixdump.pl /global/scratch/functor/dbdump.sql /global/scratch/functor/dbdump_fix.sql` . 
  
        functor@bugaboo:~> ./fixdump.pl /global/scratch/functor/dbdump.sql /global/scratch/functor/dbdump_fix.sql
        Fixes made shown
        --------------------------------------------------
        functor@bugaboo:~> 
        
 + This runs the perl script /home/functor/fixdump.pl.
 + There is also a script /home/functor/fixdump.sh .
 + This makes a fixed dump file `dbdump_fix.sql` with the required "functor" prefix for schemas.

5. Create database with "functor" prefix. 

        functor@bugaboo:~> mysql
        Welcome to the MySQL monitor.  Commands end with ; or \g.
        Your MySQL connection id is 118014
        ......
        mysql> CREATE DATABASE functor_DATABASE_NAME;
        mysql> SHOW DATABASES;

6. Run `dbdump_fix.sql` to import the schemas. This can be done from mysql or using 

        functor@bugaboo:~> mysql functor_DATABASE_NAME </global/scratch/functor/dbdump_fix.sql
