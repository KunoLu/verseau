# dataCollecter介绍



## 简介



​		`datCollcetor`是自动统计测试数据得工具。该脚本根据实际需求从`python监控脚本`（自编监控脚本：`pstat_v1.0.4`）及`JMeter`中收集`InfluxDB`监控数据并以定制格式将测试结果写入到`Excel`中。统计格式军为基准模板，如有其他格式需求请自行根据实际情况调整。



## 功能概要



​		根据UTC格式时间戳，从`InfluxDB`统计以下测试场景数据并将测试结果（`host CPU`、`host MEM`、`docker CPU`、`docker MEM`、`JMeter response time`、`JMeter TPS`）写入至`Excel`中。

1. 负载测试场景
2. 容量测试场景
3. 稳定性测试场景



## 版本



| 版本 | 完成日期   | 负责人 | 状态                                                         |
| ---- | ---------- | ------ | ------------------------------------------------------------ |
| v1.0 | 2020-05-12 | 路宋麟 | 初版                                                         |
| v1.1 | 2020-05-15 | 路宋麟 | 修复bug、新增部分字段                                        |
| v1.2 | 2020-06-03 | 路宋麟 | 修复落地数据excel表部分标题错误bug                           |
| v2.0 | 2020-12-01 | 路宋麟 | 1，修改生成的excel文件的sheet页排版<br />2，新增远程更新功能 |



# 说明文档



## 文件说明



​		解压`dataCollectoer_v2.zip`文件，`dataCollectoer_v2\dataCollector2`文件夹下得`source.zip`为工具源码，`dataCollecter2`文件夹下为脚本工具。

​		`dataCollecter_v2`目录下得文件说明如下：

| 文件                 | 说明                                                         |
| -------------------- | ------------------------------------------------------------ |
| backup文件夹         | 远程更新时，config.ini的备份目录（无需配置管理）             |
| dataCollecter2文件夹 | 脚本工具的主目录，无需远程更新时，可直接进入该目录下配置并点击dataCollecter2.exe启动工具 |
| autoUpgrade.exe      | 点击后自动开始远程更新                                       |
| update.ini           | FTP远程更新的配置文件，使用者一般无需配置管理                |

​	`dataCollecter2`工具目录下得文件说明如下：

| 文件               | 说明                                                         |
| ------------------ | ------------------------------------------------------------ |
| dataCollecter2.exe | 执行脚本，可双击执行或CMD命令行执行                          |
| config.ini         | 配置文件，脚本根据配置得内容收集测试数据并写入Excel          |
| all.log            | 执行日志文件，执行脚本后生成，可在配置文件中配置日志级别，每日自动备份，亦可删除 |
| res_excel_file     | 测试结果数据表落地得文件夹目录，可在配置文件中指定路径，不指定即为当前路径生产该文件夹，执行脚本后生成该文件夹及测试结果数据表 |
| READEME文件夹      | 该文件夹下为说明文档                                         |



## 使用说明

​		需要使用者操作得主要文件为``dataCollectoer_v2\dataCollector2\config.ini`，说明如下：

| 域                   | 字段                | 说明                                                         | 备注                                                         |
| -------------------- | ------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Default              | host                | 是否读取主机资源数据；选项：1为是，0为否                     | 亦可不填留空，与填0相同                                      |
| Default              | docker              | 是否读取容器资源数据；选项：1为是，0为否                     | 亦可不填留空，与填0相同                                      |
| Default              | jmeter              | 是否读取JMeter资源数据；选项：1为是，0为否                   | 亦可不填留空，与填0相同                                      |
| Default              | result_path         | 测试结果数据表落地路径；选项：填写即至指定路径，不填为当前路径 | 会到指定路径或当前路径新建res_excel_file文件夹，并将结果数据表落地至该文件夹中 |
| Load                 | whether_load        | 是否选取负载测试场景；选项：1为是，0为否                     | 亦可不填留空，与填0相同                                      |
| Load                 | load_users          | 负载测试用户数                                               | 如whether_load为1，则该选项必填                              |
| Load                 | start_time          | 负载测试开始时间                                             | UTC格式时间戳：%Y-%m-%d %H:%M:%S                             |
| Load                 | end_time            | 负载测试结束时间                                             | UTC格式时间戳：%Y-%m-%d %H:%M:%S                             |
| Capacity             | whether_cap         | 是否选取容量测试场景；选项：1为是，0为否                     | 亦可不填留空，与填0相同                                      |
| Capacity             | init_users          | 容量测试初始组用户数                                         | 如whether_cap为1，则该选项必填                               |
| Capacity             | each_group_interval | 每组测试用户组间得步长                                       | 例：100/120/140/160/180；则步长为20                          |
| Capacity             | groups              | 容量测试得用户组数                                           | 例：100/120/140/160/180；组数为5                             |
| Capacity             | each_group_sec      | 实际获取得每组用户下得测试数据时间段，单位：秒               | 假设每组用户运行600秒，去掉每组用户下得首尾舍弃时间各60秒，实际时间即为：600-60*2=480秒 |
| Capacity             | discard_delay_sec   | 每组用户下得首尾舍弃时间间隔，单位：秒                       | 即为上述each_group_sec下得首尾舍弃得60秒间隔时间             |
| Capacity             | start_time          | 容量测试开始时间                                             | UTC格式时间戳：%Y-%m-%d %H:%M:%S；容量测试时间戳只需提供开始时间即可，后续每组时间会根据配置文件定义得值自行计算 |
| Soak                 | whether_soak        | 是否选取稳定性测试场景；选项：1为是，0为否                   | 亦可不填留空，与填0相同                                      |
| Soak                 | have_docker         | 被测系统中是否有容器服务；选项：1为是，0为否                 | 亦可不填留空，与填0相同（该参数影响稳定性测试总数据的排版，请根据实际情况填写） |
| Soak                 | soak_users          | 稳定性测试用户数                                             | 如whether_soak为1，则该选项必填                              |
| Soak                 | start_time          | 稳定性测试开始时间                                           | UTC格式时间戳：%Y-%m-%d %H:%M:%S                             |
| Soak                 | end_time            | 稳定性测试结束时间                                           | UTC格式时间戳：%Y-%m-%d %H:%M:%S                             |
| resource_utilization | influxdb_ip         | influxdb服务器对IP                                           | 资源监控数据库信息，必填                                     |
| resource_utilization | influxdb_port       | influxdb服务器对应端口                                       | 资源监控数据库信息，必填                                     |
| resource_utilization | influxdb_user       | influxdb数据库用户                                           | 资源监控数据库信息，必填                                     |
| resource_utilization | influxdb_pwd        | influxdb数据库用户密码                                       | 资源监控数据库信息，必填                                     |
| resource_utilization | influxdb_database   | influxdb数据库                                               | 资源监控数据库信息，必填                                     |
| JMeter               | influxdb_ip         | influxdb服务器对IP                                           | JMeter监控数据库信息，必填                                   |
| JMeter               | influxdb_port       | influxdb服务器对应端口                                       | JMeter监控数据库信息，必填                                   |
| JMeter               | influxdb_user       | influxdb数据库用户                                           | JMeter监控数据库信息，必填                                   |
| JMeter               | influxdb_pwd        | influxdb数据库用户密码                                       | JMeter监控数据库信息，必填                                   |
| JMeter               | influxdb_database   | influxdb数据库                                               | JMeter监控数据库信息，必填                                   |
| JMeter               | application         | 被测试得应用名称，此值作为InfluxDB得events标记存储           | 该值非常重要！！！每次JMeter脚本得交易名称修改后，建议同步修改application得值，该值在后端监听器中修改 |
| Log                  | log_level           | 执行日志级别，可选：debug、info、error                       | 日志级别大小写输入均可，例：debug或DEBUG；如无需输出任何日志（包括报错日志）可输入warning或WARNING |



​		注意：

![image-20200512175902911](C:\Users\MSI\AppData\Roaming\Typora\typora-user-images\image-20200512175902911.png)

​		后端监听器得`application`值非常重要！建议每次`JMeter`脚本得交易名称修改后，同步修改`application`得值，该值在后端监听器中修改；

​		`application`是被测试得应用名称，此值作为`InfluxDB`得`events`标记存储，故每次测试脚本中得交易名称修改后，如`application`值未修改，则`InfluxDB`得对应`application`下得`events`中，会包含修改前及修改后得交易名称，后续执行该测试脚本，对应得`JMeter`测试数据会异常。



​		另外，建议每个线程组下设定对应得后端监听器，并给每个交易不同得线程组得后端监听器，`application`赋不同值，以确保`JMeter`测试数据收集后无异常，示例如下：

![image-20200512180420009](C:\Users\MSI\AppData\Roaming\Typora\typora-user-images\image-20200512180420009.png)

​		如上图所示，`LJJ_mix_load`线程组及`LJJ_mix_cap`线程组下均放置了对应得后端监听器；其中得`application`得值可根据实际需求自定义，如线程组中得交易均相同，`application`可定义为相同值，如两线程组中的交易不同，`application`需定义成不同值，且后续每次修改对应线程组下得交易名称后，对应得后端监听器下得`application`值亦需同步修改。



## 落地文件说明



1. 最终生成得测试结果数据以类似：`dataCollecter_20200512165939.xlsx`格式生成`Excel`表格至`res_excel_file`文件夹下，`dataCollector`为固定文件名前缀，后加生成数据表得时间戳，如需详细区分该数据表所属测试场景，自定义重命名文件名即可。
2. 无论如何配置，最终生成得结果数据表中，均存在10个`sheet`页，对应配置得测试场景数据在对应`sheet`页下，未配置获取测试数据得测试场景对应`sheet`页下为空。
3. 需要注意得是，如选择稳定性测试场景结果收集（`soak`），则`Default`域下得`host`、`docker`、`jmeter`字段必须均为1，否则`soak_total`得sheet页数据会异常。



# 更新日志



| 更新日期   | 更新内容                                                     | 备注                                                         |
| ---------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 2020-05-15 | 修复result_path字段指定路径后异常报错                        |                                                              |
| 2020-05-15 | 更新docker容器资源使用率名称格式                             | 1，原为：containName-containId<br />更新为：dockerHostIP-containName-containId<br />2，版本更新为v1.1 |
| 2020-06-03 | 修复落地数据excel表load、cap、soak场景结果中部分标题错误bug  | 版本更新为v1.2                                               |
| 2020-12-01 | 1，修改生成的excel文件的sheet页排版<br />2，新增远程更新功能 | 版本更新为v2.0                                               |

