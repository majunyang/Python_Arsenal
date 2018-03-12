#! encoding:utf8

# ===========================
# Import some package
# ===========================

# ===========================
# --> for character encoding
# ===========================
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

# ===========================
# --> for Linux SSH
# ===========================
import paramiko

# ===========================
# --> for Linux
# ===========================
import os
import datetime

# ===========================
# --> for Database Oracle
# ===========================
import cx_Oracle

# ===========================
# --> for Function
# ===========================
import re

# ===========================
# Define Variables
# ===========================

# Direcotry Path
path_current_py_script = os.path.split(os.path.realpath(__file__))[0]

# --> 存放数据库SQL查询口令的路径（目录）
path_db_sql = path_current_py_script + "/sql_data"

# File Path
file_db_target = path_current_py_script + "/db_oracle.conf"
file_os_target = path_current_py_script + "/os_linux.conf"

# Threshold
# 0 - ok
# 1 - warning
# 2 - error

# --> about threshold: error

# linux: mount point - df
threshold_df = 90

# database oracle: tablespace
threshold_db_tablespace_usage = 90

# database oracle: instance

# is Oracle Instance OPEN?
threshold_db_oracle_instance_status = "OPEN"

# ===========================
# Define Functions
# ===========================

# 检查目录是否存在，如果不存在，就创建
def do_directory(path_string):
    # Function Init:
    print("")
    print("===========")
    print("Function: do_directory")
    print("===========")
    print("")

    if os.path.exists(path_string):
        print("目录【存在】")
    else:
        print("目录【不存在】")
        print("--> 创建目录：【"+path_string+"】")
        os.makedirs(path_string)

    # Function Ending.

# 处理文件数据
def do_file_config(file_path_string):
    # Variable
    object_return = open(file_path_string)

    # Return
    return object_return

    # Function Ending

# check if threshold is ok
# vector
# + means if current_status > threshold
# - means if current_status < threshold
def check_threshold(current_status,threshold_edge,vector):

    # Init
    #print("")
    #print("===========")
    #print("Function: check_threshold")
    #print("===========")
    #print("")

    # variable

    # return singal
    # default is : ok - 0
    signal_result = 0

    # Before Produce
    #print("**********")
    #print("Before Product")
    #print("**********")
    #print("Result Signal is: [" + str(signal_result) + "]")

    # Display: for Programming Troubleshooting
    #print("Vector is ["+vector+"]")
    #print("--------")
    #print("Current is ["+str(current_status)+"]")
    #print("Threshold is [" + str(threshold_edge) + "]")

    # Just do it
    if vector == "+":
        if current_status > threshold_edge:
            signal_result=2
    if vector == "-":
        if current_status < threshold_edge:
            signal_result = 2

    # After Produce
    #print("**********")
    #print("After Product")
    #print("**********")
    #print("Result Signal is: ["+str(signal_result)+"]")

    # Befor finished
    #print("")

    # Return
    return signal_result

    # Function ending.

# Do SSH Execute and return Result
def do_ssh(ip, port, user, password, command_string):

    # Function Init:
    print("")
    print("===========")
    print("Function: do_ssh")
    print("===========")
    print("")

    # Variable
    data_result = ""

    # Paramiko: Init

    object_paramiko = paramiko.SSHClient()
    object_paramiko.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect
    object_paramiko.connect(ip, port, user, password, timeout=2)

    # Execute Command
    stdin, stdout, stderr = object_paramiko.exec_command(command_string)

    data_result = stdout.readlines()

    # Close Connect
    object_paramiko.close()

    # Before ending
    #print("")

    # Return
    return data_result

    # Function ending.

# 数据库检查：表空间使用率
def check_db_oracle_tablespace_usage(db_oracle_cursor):
    # Function Init:
    print("")
    print("===========")
    print("Function: check_db_oracle_tablespace_usage")
    print("===========")
    print("")

    # Variable
    file_sql_command = path_db_sql + "/db_oracle_tablespace_usage.sql"

    file_obj = open(file_sql_command,'r')
    file_data = file_obj.read()

    db_oracle_cursor.execute(file_data)

    data_result = db_oracle_cursor.fetchall()

    for tbs_item in data_result:
        # variable
        signal_threshold = 0

        tbs_name = str(tbs_item).split()[0].strip().strip('(').strip('\'').strip(',').strip('\'')
        tbs_space_sum_mb = str(tbs_item).split()[1].strip(',')
        tbs_space_used_mb = str(tbs_item).split()[2].strip(',')
        tbs_space_free_mb = str(tbs_item).split()[3].strip(',')
        tbs_space_used_percent = str(str(tbs_item).split()[4]).strip().strip(')')

        # display
        print("******")
        print("表空间【"+tbs_name+"】，总容量【"+tbs_space_sum_mb+"】 - 已使用："+tbs_space_used_mb+"，当前剩余："+tbs_space_free_mb+" - 使用率："+tbs_space_used_percent)

        # About Threshold
        print("阈值 - 使用率：【"+str(threshold_db_tablespace_usage)+"】")

        #print("阈值检查 - Before：【" + str(signal_threshold) + "】")

        # Do Threshold
        signal_threshold = check_threshold(float(tbs_space_used_percent),threshold_db_tablespace_usage,"+")

        # display
        #print("阈值检查 - After：【"+str(signal_threshold)+"】")

        if signal_threshold == 2:
            print("### 触发阈值")
        else:
            print("### 状态正常")


        # before end
        #print("")

        # End Loop

    # Before Ending
    #print("")

    # Return
    return data_result

    # Function Ending.

# 基础函数：时间差额比较
def diff_times(before_date,after_date):

    # variable
    result_string = ""

    # Time before
    datetime_time_before = datetime.datetime.strptime(before_date,'%Y-%m-%d %H:%M:%S')

    # Time after
    datetime_time_after = datetime.datetime.strptime(after_date, '%Y-%m-%d %H:%M:%S')

    # The diff
    datetime_time_diff = datetime_time_after - datetime_time_before

    # Analyze
    if datetime_time_diff.days == 0:
        datetime_time_diff_hour = datetime_time_diff.seconds/60/60
        result_string = str(datetime_time_diff_hour) + " 小时"
    else:
        result_string = str(datetime_time_diff.days) + " 天"

    # Return
    return result_string

    # Function end.

# 根据文件名的部分字符，在指定的目录中搜寻完整的文件路径
def find_file_in_directory(ip,port,user,password,directory_path,filename_str):

    # variable

    cmd_str = "ls "+directory_path+" | grep "+filename_str

    # On local
    #list_file_all = os.listdir(directory_path)

    # On remote
    list_file_all = do_ssh(ip,port,user,password,cmd_str)

    # Target Filename
    target_filename = str(list_file_all).split()[0].strip('[]').split('\'')[1].split('\\')[0]

    path_target_file = directory_path + "/" + target_filename

    # Return String is:
    return_string = "Alert文件路径为：" + path_target_file

    # Display

    # Old

    #print("variable: direcotry_path is: 【"+directory_path+"】")
    #print("---------")
    #print("The File is::【"+target_filename+"】")
    #print("---------")
    #print(list_file_all)
    #print("++++++++++++++++++++++++++")

    # New
    print(return_string)

    # Do

    #for file_item in list_file_all:

        # Display
        #print("当前获得的对象：【"+file_item+"】")

    # Return
    return return_string

    # Function end.

# 根据IP信息在主机配置文件中获取相关连接信息
def get_server_connect_info_by_ip(ip_str):

    # variable
    return_data = ""
    file_data = open(file_os_target)
    target_line = ""

    for line in file_data.readlines():
        if re.findall(ip_str,line):
            target_line = line

    # Display
    #print("Target Line is:【"+target_line+"】")

    # Be ready
    return_data = target_line.split()

    # Display
    #print("Return data is:【"+str(return_data)+"】")

    # Return
    return return_data

    # Function end

# 检查数据库状态 - 时间部分
def check_db_oracle_instance_status_part_1_time(db_time_create,db_time_startup):
    # Function Init:
    print("")
    print("===========")
    print("Function: check_db_oracle_instance_status_part_1_time")
    print("===========")
    print("")

    # variable
    time_current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Analyze
    str_time_create = diff_times(db_time_create,time_current)
    str_time_startup = diff_times(db_time_startup,time_current)

    # Display
    print("运行了多长时间？自【创建】以来：【" + str_time_create + "】")
    print("运行了多长时间？自【启动】以来：【" + str_time_startup + "】")

    # Function end.

# 检查数据库状态 - 实例名称
def check_db_oracle_instance_status_part_4_name_db_instance(db_name,instance_name):
    # Function Init:
    print("")
    print("===========")
    print("Function: check_db_oracle_instance_status_part_4_name_db_instance")
    print("===========")
    print("")

    # Display
    print("数据库名称是：【" + db_name + "】")
    print("实例名称是：【" + instance_name + "】")

    # Function end.

# 检查数据库状态 - 实例状态
def check_db_oracle_instance_status_part_2_instance_stauts(current_status):
    # Function Init:
    print("")
    print("===========")
    print("Function: check_db_oracle_instance_status_part_2_instance_stauts")
    print("===========")
    print("")

    # variable
    result_string = ""

    if current_status == threshold_db_oracle_instance_status:
        result_string = "数据库当前状态为【"+current_status+"】，运行【正常】"
    else:
        result_string = "数据库当前状态为【" + current_status + "】，运行【不正常】"

    # Display
    print(result_string)

    # Before ending
    #print("")

    # Return
    return result_string

    # Function ending.

# 检查数据库状态 - 架构：DG
def check_db_oracle_instance_status_part_3_is_DataGuard(current_status):
    # Function Init:
    print("")
    print("===========")
    print("Function: check_db_oracle_instance_status_part_3_is_DataGuard")
    print("===========")
    print("")

    # variable
    result_string = ""

    if current_status == "UNPROTECTED":
        result_string = "当前数据库架构【不是】：【Data Guard】"
    else:
        result_string = "当前数据库架构【是】：【Data Guard】"

    # Display
    print(result_string)

    # Before ending
    #print("")

    # Return
    return result_string

    # Function ending.

# 检查数据库状态 - 架构：DG
def check_db_oracle_instance_status_part_5_version(version_str):
    # Function Init:
    print("")
    print("===========")
    print("Function: check_db_oracle_instance_status_part_5_version")
    print("===========")
    print("")

    # variable
    result_string = "数据库版本是：【" + version_str + "】"

    # Display
    print(result_string)

    # Before ending
    #print("")

    # Return
    return result_string

    # Function ending.

# 数据库检查：数据库实例状态
def check_db_oracle_instance_status(db_oracle_cursor):
    # Function Init:
    print("")
    print("===========")
    print("Function: check_db_oracle_instance_status")
    print("===========")
    print("")

    # Variable
    file_sql_command = path_db_sql + "/db_oracle_instance_status.sql"

    file_obj = open(file_sql_command, 'r')
    file_data = file_obj.read()

    db_oracle_cursor.execute(file_data)

    data_result = db_oracle_cursor.fetchall()

    for item in data_result:

        # display - One

        # print("Result:")
        print(item)

        # variable

        # database metainfo
        db_instance_dbid = str(item).split(',')[0].strip(',').strip('(')
        db_instance_inst_id = str(item).split(',')[1].strip(',')
        db_instance_instance_number = str(item).split(',')[2].strip(',')
        db_instance_db_name = str(item).split(',')[3].strip(',').split('\'')[1]
        db_instance_db_unique_name = str(item).split(',')[4].strip(',')
        db_instance_instance_name = str(item).split(',')[5].strip(',').split('\'')[1]
        db_instance_host_name = str(item).split(',')[6].strip(',')
        db_instance_current_scn = str(item).split(',')[7].strip(',')
        db_instance_time_created = str(item).split(',')[8].strip(',').split('\'')[1]
        db_instance_time_startup = str(item).split(',')[9].strip(',').split('\'')[1]
        db_instance_status = str(item).split(',')[10].strip(',').split('\'')[1]
        db_instance_open_mode = str(item).split(',')[11].strip(',')
        db_instance_database_status = str(item).split(',')[12].strip(',')
        db_instance_log_mode = str(item).split(',')[13].strip(',')
        db_instance_force_logging = str(item).split(',')[14].strip(',')
        db_instance_flashback_on = str(item).split(',')[15].strip(',')
        db_instance_database_role = str(item).split(',')[16].strip(',')
        db_instance_instance_role = str(item).split(',')[17].strip(',')
        db_instance_active_state = str(item).split(',')[18].strip(',')
        db_instance_blocked = str(item).split(',')[19].strip(',')
        db_instance_protection_level = str(item).split(',')[20].strip(',').split('\'')[1]
        db_instance_version = str(item).split(',')[21].strip(',').split('\'')[1]

        # Testing
        #print("Protection Level is: 【"+db_instance_protection_level+"】")
        #print("Protection Level is: 【" + db_instance_version + "】")

        # =========================================
        # 数据库状态：细分项目 - 检查

        # 数据库的名称相关信息
        check_db_oracle_instance_status_part_4_name_db_instance(db_instance_db_name,db_instance_instance_name)

        # 数据库的版本信息的处理
        check_db_oracle_instance_status_part_5_version(db_instance_version)

        # 时间信息检查
        check_db_oracle_instance_status_part_1_time(db_instance_time_created,db_instance_time_startup)

        # 数据库实例状态检查
        check_db_oracle_instance_status_part_2_instance_stauts(db_instance_status)

        # 数据库架构：是否是DG
        check_db_oracle_instance_status_part_3_is_DataGuard(db_instance_protection_level)

        # Loop FOR ending.

    # Before Ending
    #print("")

    # Function Ending.

# 数据库检查：数据库架构，是否是RAC
def check_db_oracle_instance_status_isRAC(db_oracle_cursor):
    # Function Init:
    print("")
    print("===========")
    print("Function: check_db_oracle_instance_status_isRAC")
    print("===========")
    print("")

    # Variable
    file_sql_command = path_db_sql + "/db_oracle_instance_status_isRAC.sql"

    file_obj = open(file_sql_command, 'r')
    file_data = file_obj.read()

    db_oracle_cursor.execute(file_data)

    data_result = db_oracle_cursor.fetchall()

    result_str = ""

    for item in data_result:

        # Testing
        #print(item)

        # Variable
        signal_str = str(item).split(',')[1].split('\'')[1]

        # Analyze
        if signal_str == "TRUE":
            result_str = "当前数据库【是】RAC架构"

        if signal_str == "FALSE":
            result_str = "当前数据库【不是】RAC架构"

        # display
        #print(signal_str)
        #print(result_str)

    # display
    print(result_str)

    # Return
    return result_str

    # Function Ending

# 数据库检查：文件，控制文件
def check_db_oracle_file_controlfile(db_oracle_cursor):
    # Function Init:
    print("")
    print("===========")
    print("Function: check_db_oracle_file_controlfile")
    print("===========")
    print("")

    # Variable
    file_sql_command = path_db_sql + "/db_oracle_file_controlfile.sql"

    file_obj = open(file_sql_command, 'r')
    file_data = file_obj.read()

    db_oracle_cursor.execute(file_data)

    data_result = db_oracle_cursor.fetchall()

    list_controlfile = str(data_result).split()
    control_file_target = []

    result_str = ""

    for item in list_controlfile:
        # Testing
        #print("【"+item+"】")

        # Analyze
        middle_state_item = item.strip('[]').split('\'')[1]

        # Display
        #print("【"+middle_state_item+"】")

        # Set
        #control_file_target = middle_state_item + " "
        control_file_target.append(middle_state_item)

        #for i in middle_state_item:
            # display

            #print("---")
            #print(i)

            # set

            #control_file_target = i + " "

        # Variable

        # Analyze

        # display
        # print("Now we get:【"+db_parameter_value+"】")
        # print(result_str)

        # For LOOP end

    # set
    result_str = "控制文件为：【"+str(control_file_target)+"】"

    # display
    print(result_str)

    # Return
    return control_file_target

    # Function Ending

# 数据库检查：文件，联机日志文件
def check_db_oracle_file_redo(db_oracle_cursor):
    # Function Init:
    print("")
    print("===========")
    print("Function: check_db_oracle_file_redo")
    print("===========")
    print("")

    # variable
    return_data = ""

    list_column_file_name = []

    # from file
    sql_file = path_db_sql + "/db_oracle_file_redo.sql"

    file_session = open(sql_file, 'r')


    file_data = file_session.read()

    # open database session
    db_oracle_cursor.execute(file_data)

    db_result_set = db_oracle_cursor.fetchall()

    # read result set
    for result_item in db_result_set:
        # Variable
        column_file_name = str(result_item).split()[3].strip('\'').split('\'')[0]

        # Display
        #print("%%%%%%%%%%%%%%%")
        #print(result_item)
        #print(str(result_item).split()[3].strip('\'').split('\'')[0])

        # Analyze
        list_column_file_name.append(column_file_name)


    # Return something
    return list_column_file_name

    # Function Finished

# 数据库检查：文件，参数文件
def check_db_oracle_file_spfile(db_oracle_cursor):
    # Function Init:
    print("")
    print("===========")
    print("Function: check_db_oracle_file_spfile")
    print("===========")
    print("")

    # Variable
    file_sql_command = path_db_sql + "/db_oracle_file_spfile.sql"

    file_obj = open(file_sql_command, 'r')
    file_data = file_obj.read()

    db_oracle_cursor.execute(file_data)

    data_result = db_oracle_cursor.fetchall()

    result_str = ""

    for item in data_result:
        # Testing
        #print(item)

        # Variable
        db_parameter_value = str(item).split(',')[3].split('\'')[1]
        result_str = "参数文件：【"+db_parameter_value+"】"
        # Analyze

        # display
        #print("Now we get:【"+db_parameter_value+"】")
        #print(result_str)

        # For LOOP end

    # display
    print(result_str)

    # Return
    return result_str

    # Function Ending

# 数据库检查：文件，数据文件
def check_db_oracle_file_datafile(db_oracle_cursor):
    # Function Init:
    print("")
    print("===========")
    print("Function: check_db_oracle_file_datafile")
    print("===========")
    print("")

    # variable
    return_data = ""

    list_column_file_name = []

    # from file
    sql_file = path_db_sql + "/db_oracle_file_datafile.sql"

    file_session = open(sql_file, 'r')

    file_data = file_session.read()

    # open database session
    db_oracle_cursor.execute(file_data)

    db_result_set = db_oracle_cursor.fetchall()

    # read result set
    for result_item in db_result_set:
        # Variable
        column_file_name = str(result_item).split()[0].strip('\'').split('\'')[1]

        # Display
        #print("%%%%%%%%%%%%%%%")
        #print(result_item)
        #print(str(result_item).split()[3].strip('\'').split('\'')[0])

        # Analyze
        list_column_file_name.append(column_file_name)

    # Return something
    return list_column_file_name

    # Function Finished

# 数据库检查：文件，日志文件 - Alert
def check_db_oracle_file_log_alert(db_oracle_cursor,ip_str):
    # Function Init:
    print("")
    print("===========")
    print("Function: check_db_oracle_file_log_alert")
    print("===========")
    print("")

    # Variable
    file_sql_command = path_db_sql + "/db_oracle_file_alert.sql"

    file_obj = open(file_sql_command, 'r')
    file_data = file_obj.read()

    db_oracle_cursor.execute(file_data)

    data_result = db_oracle_cursor.fetchall()

    result_str = ""

    for item in data_result:
        # Testing
        #print(item)

        # Variable
        db_log_alert_dir = str(item).split(',')[3].split('\'')[1]

        # about what we return
        #result_str = "日志文件 - Alert：【"+db_parameter_value+"】"

        # variable middle state

        # way one
        #target_ip = get_server_connect_info_by_ip(ip_str)[0]
        #target_port = get_server_connect_info_by_ip(ip_str)[1]
        #target_user = get_server_connect_info_by_ip(ip_str)[2]
        #target_passwd = get_server_connect_info_by_ip(ip_str)[3]

        # way two
        target_ip, target_port, target_user, target_passwd = get_server_connect_info_by_ip(ip_str)

        # display
        #print("IP:"+target_ip)
        #print("Port:" + target_port)
        #print("User:" + target_user)
        #print("Password:" + target_passwd)

        # Do Find
        find_file_in_directory(target_ip, target_port, target_user, target_passwd,db_log_alert_dir,"alert")

        # display
        #print("Now we get:【"+db_log_alert_dir+"】")
        #print(result_str)

        # For LOOP end

    # display
    #print(result_str)

    # Return
    return result_str

    # Function Ending

# 处理Linux巡检
def check_os_linux():

    # Function Init:
    print("")
    print("===========")
    print("Function: check_os_linux")
    print("===========")
    print("")

    with do_file_config(file_os_target) as file_data:

        # variable
        loop_1_count = 1

        # Get per line data
        for line in file_data.readlines():

            # Init
            print("**** Current 【" + str(loop_1_count) + "】 ****")

            # Display
            #print("Line Data is:")
            #print(line)

            # Variable
            os_target_ip = line.split()[0]
            os_target_port = line.split()[1]
            os_target_user = line.split()[2]
            os_target_passwd = line.split()[3]

            # Display
            print("-------------")
            print("IP：" + os_target_ip)
            print("端口：" + os_target_port)
            print("用户：" + os_target_user)
            print("密码：" + os_target_passwd)
            print("-------------")

            # Loop FOR ending.

    # Function Ending.

# 处理【Database - Oracle】巡检
def check_db_oracle():

    # Function Init:
    print("")
    print("===========")
    print("Function: check_db_oracle")
    print("===========")
    print("")

    with do_file_config(file_db_target) as file_data:

        # variable
        loop_1_count = 1

        # Get per line data
        for line in file_data.readlines():

            # Init
            print("**** Current 【" + str(loop_1_count) + "】 ****")

            # Display
            #print("Line Data is:")
            #print(line)

            # Variable
            db_target_ip = line.split()[0]
            db_target_port = line.split()[1]
            db_target_tns = line.split()[2]
            db_target_user = line.split()[3]
            db_target_passwd = line.split()[4]

            # Display
            print("-------------")
            print("IP：" + db_target_ip)
            print("端口：" + db_target_port)
            print("实例（TNS）："+db_target_tns)
            print("用户：" + db_target_user)
            print("密码：" + db_target_passwd)
            print("-------------")

            # cx_Oracle - 连接Oracle数据库
            try:
                database_connection = cx_Oracle.connect(db_target_user + '/' + db_target_passwd + '@' + db_target_ip + ':' + db_target_port + '/' + db_target_tns, mode=cx_Oracle.SYSDBA)
            except:
                message_error = ("Error：TNSNAME [" + str(db_target_tns) + "] is Unreachable, The reason may be: " + str(e)).strip()
                print(message_error)
            else:
                database_cursor = database_connection.cursor()

                # Testing
                #sql_result = check_db_oracle_tablespace_usage(database_cursor)

                # 检查：数据库实例状态
                check_db_oracle_instance_status(database_cursor)

                # 检查：数据库架构，是否是RAC
                check_db_oracle_instance_status_isRAC(database_cursor)

                # 检查：表空间使用率
                check_db_oracle_tablespace_usage(database_cursor)

                # 检查：文件 - 参数文件的位置
                check_db_oracle_file_spfile(database_cursor)

                # 检查：文件 - 日志文件 -Alert
                check_db_oracle_file_log_alert(database_cursor,db_target_ip)

                # 检查：文件 - 控制文件
                check_db_oracle_file_controlfile(database_cursor)

                # 检查：文件 - 联机日志文件
                #check_db_oracle_file_redo(database_cursor)
                print(str(check_db_oracle_file_redo(database_cursor)))

                # 检查：文件 - 数据文件
                #check_db_oracle_file_datafile(database_cursor)
                print(str(check_db_oracle_file_datafile(database_cursor)))


                # Display
                #for i in sql_result:
                #    print(i)

                # Close
                #database_cursor.close()
                #database_connection.close()

            # Loop FOR ending.

    # Before Ending
    print("")

    # Function Ending.

# ===========================
# Test: Uppon
# ===========================

# ----------------------------
# 测试：check_threshold

# if less than threshold, warning

#print("1")
#check_threshold(80,threshold_df,"-")

#print("2")
#check_threshold(91,threshold_db_tablespace_usage,"-")

# if larger than threshold, warning

#print("3")
#check_threshold(80.3,threshold_df,"+")

#print("4")
#check_threshold(91.45,threshold_db_tablespace_usage,"+")

# ----------------------------
# 测试: do_ssh

#result = do_ssh("192.168.174.130",22,"root","oracle","ifconfig")
#print("Result is:")
#print(result)

# ----------------------------
# 测试： do_directory

#do_directory("F:/Lenka_she/Shang_Hai")

# ----------------------------
# 测试： check_os_linux

#check_os_linux()

# ----------------------------

# ----------------------------

# ----------------------------

# ----------------------------

# ----------------------------

# ----------------------------

# ----------------------------

# ----------------------------

# ----------------------------

# ----------------------------

# ----------------------------

# ----------------------------

# ----------------------------

# ===========================
# Acture Do something
# ===========================

# Python：Main
if __name__ == '__main__':

    # Init
    #print("Python: Main() 方法")
    print("Python：数据库与操作系统（Linux） - 巡检")

    # About Directory
    do_directory(path_db_sql)

    # Check Linux
    check_os_linux()

    # Check Database Oracle
    check_db_oracle()


# ===========================
# Finished
# ===========================