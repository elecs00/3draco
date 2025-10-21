import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    pkg_share_gazebo = get_package_share_directory('slampibot_gazebo')
    pkg_gazebo_ros = FindPackageShare(package='gazebo_ros').find('gazebo_ros')    
    
    urdf_xacro = os.path.join(pkg_share_gazebo, 'urdf', 'spb_urdf_gazebo.xacro')
    rviz_config = os.path.join(pkg_share_gazebo, 'rviz', 'spb_urdf_map.rviz')    
    world_file = os.path.join(pkg_share_gazebo, "worlds", "spb_building_slampibot.world")
    
    cartographer_config = LaunchConfiguration('cartographer_config', default=os.path.join(pkg_share_gazebo, 'params'))
    
    # 🌟 1. LUA 설정 파일 이름을 3D용으로 변경합니다. (파일 이름이 바뀌었다고 가정)
    lua_config = LaunchConfiguration('lua_config', default='spb_cartographer_3d_gazebo.lua') # 파일명 수정
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    world = LaunchConfiguration('world')
    
    dla_world = DeclareLaunchArgument(
        name='world',
        default_value=world_file,
        description='Full path to the world model file to load'
    )
    
    dla_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )
    
    # Start Gazebo server
    gazebo_server_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')),
        launch_arguments={'world': world}.items()
    )

    # Start Gazebo client    
    gazebo_client_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py'))
    )

    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time, 
                     'robot_description': Command(['xacro',' ', urdf_xacro])}])

    rviz_cmd = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config])
    
    rqt_robot_steering_cmd = Node(
        package='rqt_robot_steering',
        executable='rqt_robot_steering',
        name='rqt_robot_steering',
        output='screen')
    
    cartoprapher_cmd = Node(
        package='cartographer_ros', 
        executable='cartographer_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-configuration_directory', cartographer_config,
                '-configuration_basename', lua_config],
    # ----------------------------------------------------
    # 🌟 수정 1: 'remaps' 대신 올바른 인자 'remappings'를 사용합니다.
    # 🌟 수정 2: 'points2' 토픽을 압축 해제된 토픽으로 연결합니다.
    # ----------------------------------------------------
        remappings=[('points2', '/out/draco/decompressed')]
    )
        
    # 🌟 2. 2D OccupancyGrid를 생성하는 노드를 제거합니다. (3D SLAM에는 불필요)
    # occupancy_grid_cmd = Node(
    #     package='cartographer_ros',
    #     executable='cartographer_occupancy_grid_node',
    #     name='cartographer_occupancy_grid_node',
    #     output='screen',
    #     parameters=[{'use_sim_time': use_sim_time}],
    #     arguments=['-resolution', '0.02', '-publish_period_sec', '1.0'])
    
    ld = LaunchDescription()
    
    ld.add_action(dla_use_sim_time)
    ld.add_action(dla_world)
    #ld.add_action(gazebo_server_cmd)
    #ld.add_action(gazebo_client_cmd)
    ld.add_action(robot_state_publisher_cmd)    
    ld.add_action(cartoprapher_cmd)
    # ld.add_action(occupancy_grid_cmd) # 2D 지도 생성 노드 제거
    ld.add_action(rviz_cmd)
    ld.add_action(rqt_robot_steering_cmd)

    return ld
