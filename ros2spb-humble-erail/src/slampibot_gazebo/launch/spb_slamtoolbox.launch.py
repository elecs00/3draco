import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    pkg_share = FindPackageShare(package='slampibot_gazebo').find('slampibot_gazebo')
    urdf_xacro = os.path.join(pkg_share, 'urdf', 'spb_urdf_gazebo_spawn.xacro')

    # rosbag 재생 시 시뮬레이션 시간을 사용하도록 설정
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # SLAM 설정 파일 경로
    slam_params_file = LaunchConfiguration('slam_params_file')
    
    # rf2o odometry 실행
    rf2o_launch_dir = os.path.join(get_package_share_directory('rf2o_laser_odometry'), 'launch')
    
    # rviz 설정 파일 경로
    rviz_config_dir = os.path.join(
        get_package_share_directory('slampibot_gazebo'),
        'rviz',
        'slampibot_slamtoolbox_map.rviz')

    declare_use_sim_time_argument = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation/Gazebo clock')
        
    declare_slam_params_file_cmd = DeclareLaunchArgument(
        'slam_params_file',
        default_value=os.path.join(get_package_share_directory("slampibot_gazebo"),
                                   'params', 'mapper_params_online_async.yaml'),
        description='Full path to the ROS2 parameters file to use for the slam_toolbox node')

    # Joint State Publisher
    joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_sim_time': use_sim_time}],
    )

    # Robot State Publisher
    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time, 
                     'robot_description': Command(['xacro',' ', urdf_xacro])}])

    # rf2o_laser_odometry 노드 실행
    start_rf2o_laser_odometry_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(rf2o_launch_dir, 'rf2o_laser_odometry.launch.py')),
        launch_arguments={
            'use_sim_time': use_sim_time
        }.items()
    )

    # slam_toolbox 노드 실행
    start_async_slam_toolbox_node = Node(
        parameters=[
          slam_params_file,
          {'use_sim_time': use_sim_time}
        ],
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        remappings=[
            # odom 토픽을 rf2o_laser_odometry에서 오는 토픽으로 리매핑
            ('/odom', '/rf2o_laser_odometry/odom')
        ])

    # Rviz 실행
    start_rviz_cmd = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_dir],
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
        )

    ld = LaunchDescription()

    ld.add_action(declare_use_sim_time_argument)
    ld.add_action(declare_slam_params_file_cmd)
    
    ld.add_action(joint_state_publisher_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(start_rf2o_laser_odometry_cmd)
    ld.add_action(start_async_slam_toolbox_node)
    ld.add_action(start_rviz_cmd)

    return ld