#!/bin/bash
#touch script.sh && chmod +x script.sh && vim script.sh

dir=/outputTestMapReduce
directory=/usr/share/hadoop
log=$dir/log.txt

case $1 in
        mr)
                FUNC="map_reduce"
        ;;
        pi)
                FUNC="run_pi_job"
        ;;
        gn)
                FUNC="get_job_name"
        ;;
        lt)
                FUNC="get_list_active_trackers"
        ;;
        ed)
                FUNC=" check_exist_directory"
        ;;
esac

shift

until [ -z $1 ]
do
        if [ "$1" = "-nc" ]
        then
                NODE_COUNT="$2"
                shift
        fi

        if [ "$1" = "-jn" ]
        then
                JOB_NAME="$2"
                shift
        fi

        shift
done

f_var_check() {
        case "$1" in
                v_node_count)
                        if [ -z "$NODE_COUNT" ]
                        then
                                echo "count_of_node_not_specified"
                                exit 0
                        fi
                ;;
                v_job_name)
                        if [ -z "$JOB_NAME" ]
                        then
                                echo "job_name_not_specified"
                                exit 0
                        fi
                ;;
        esac
}

f_create_log_dir() {
rm -r $dir 2>/dev/null
mkdir $dir
chmod -R 777 $dir
touch $log
}

map_reduce() {
f_create_log_dir
echo "[------ dpkg------]">>$log
echo `dpkg --get-selections | grep hadoop` >>$log
echo "[------jps------]">>$log
echo `jps | grep -v Jps` >>$log
echo "[------netstat------]">>$log
echo `sudo netstat -plten | grep java` &>>$log
echo "[------test for hdfs------]">>$log
echo `dmesg > $dir/input` 2>>$log
su -c "hadoop dfs -ls /" hadoop &&
su -c "hadoop dfs -mkdir /test" hadoop &&
su -c "hadoop dfs -copyFromLocal $dir/input /test/mydata" hadoop 2>>$log
echo "[------start job------]">>$log &&
su -c "cd $directory && hadoop jar hadoop-examples-1.1.1.jar wordcount /test/mydata /test/output" hadoop 2>>$log &&
su -c "hadoop dfs -copyToLocal /test/output/ $dir/out/" hadoop 2>>$log &&
su -c "hadoop dfs -rmr /test" hadoop 2>>$log
}

run_pi_job() {
f_var_check v_node_count
f_create_log_dir
su -c "cd $directory && hadoop jar hadoop-examples-1.1.1.jar pi $[$NODE_COUNT*10] 1000" hadoop 2>>$log
}

get_job_name() {
su -c "cd $directory && hadoop job -list all | tail -n1" hadoop | awk '{print $1}' 2>>$log
}

get_list_active_trackers() {
f_create_log_dir
sleep 30 &&
su -c "cd $directory && hadoop job -list-active-trackers" hadoop | wc -l 2>>$log
}

check_exist_directory() {
f_var_check v_job_name
if ! [ -d /mnt/log/hadoop/hadoop/userlogs/$JOB_NAME ];
then echo "directory_not_found" && exit 1
fi
}

$FUNC