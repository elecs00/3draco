include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",
  tracking_frame = "imu_link",  -- 3D SLAM은 IMU를 주로 사용하므로 변경 (이전: lidar_link)
  published_frame = "odom",    
  odom_frame = "odom",
  provide_odom_frame = false,  
  publish_frame_projected_to_2d = false, -- 3D 지도를 사용하므로 2D 투영 비활성화 (이전: true)
  use_odometry = true,  
  use_nav_sat = false,
  use_landmarks = false,

  -- 입력 데이터 설정 (3D PointCloud2 사용)
  num_laser_scans = 0,               -- 2D LaserScan 비활성화 (이전: 1)
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 1,              -- 3D PointCloud2 활성화 (이전: 0)
  num_subdivisions_per_point_cloud = 1, -- PointCloud2에 대한 분할 수

  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,
  rangefinder_sampling_ratio = 1.,
  odometry_sampling_ratio = 1.,
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 1.,
  landmarks_sampling_ratio = 1.,
}

-- 3D Builder 활성화 및 스레드 증가
MAP_BUILDER.use_trajectory_builder_3d = true -- 3D SLAM 활성화 (이전: use_trajectory_builder_2d = true)
MAP_BUILDER.num_background_threads = 8 -- 3D 처리를 위해 증가 권장

-- [[ 3D Trajectory Builder 설정 ]]
-- 2D 관련 파라미터는 삭제하고 3D 전용 파라미터 추가

TRAJECTORY_BUILDER_3D.min_range = 0.5
TRAJECTORY_BUILDER_3D.max_range = 30.0
TRAJECTORY_BUILDER_3D.missing_data_ray_length = 5.0
TRAJECTORY_BUILDER_3D.use_imu_data = true -- 3D SLAM에서 IMU 사용 (필수)
TRAJECTORY_BUILDER_3D.scans_per_gravity_alignment = 10
TRAJECTORY_BUILDER_3D.motion_filter.max_angle_radians = math.rad(0.1)

-- Voxel Filter: 입력 PointCloud의 해상도를 낮춰 처리 속도 향상
TRAJECTORY_BUILDER_3D.voxel_filter_size = 0.05 

-- Local Scan Matcher (Ceres) 설정
TRAJECTORY_BUILDER_3D.ceres_scan_matcher.translation_weight = 1e5
TRAJECTORY_BUILDER_3D.ceres_scan_matcher.rotation_weight = 1e5
TRAJECTORY_BUILDER_3D.ceres_scan_matcher.occlusion_filter_config = {
  min_z = 0.2,
  max_z = 2.0,
  width = 0.5,
  height = 0.5,
  }

-- Global SLAM (Pose Graph) 설정
POSE_GRAPH.constraint_builder.min_score = 0.65
POSE_GRAPH.constraint_builder.global_localization_min_score = 0.7
-- 3D는 계산량이 많아 샘플링 비율을 낮추는 것이 일반적
POSE_GRAPH.constraint_builder.sampling_ratio = 0.03 

return options
