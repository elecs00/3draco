ROS2 Draco Project
📌 프로젝트 개요

ROS2_Draco_Project는 ROS 2 환경에서 Google Draco를 활용하여 PointCloud2 메시지를 효율적으로 압축하고 전송하는 시스템입니다.
저대역폭 환경에서도 3D 센서 데이터를 빠르고 안정적으로 처리할 수 있도록 설계되었습니다.

🛠 설치 및 빌드

의존성 설치

sudo apt install 
                 ros-humble-point-cloud-transport \
                 ros-humble-draco-point-cloud-transport \
                 ros-humble-point-cloud-to-laserscan


워크스페이스 빌드

cd draco_ws
colcon build
source install/setup.bash

💡 실행 방법
1. rosbag 파일 실행
  ros2 bag play rosbag2_2024_09_24-14_28_57_0.db3 --clock

2. Draco 압축 / 재전송 노드 실행
ros2 run point_cloud_transport republish --ros-args \
  --remap in:=/sensing/lidar/top/pointcloud \
  --remap out:=pct/point_cloud \
  -p in_transport:=raw \
  -p out_transport:=draco

토픽	방향	설명

  /sensing/lidar/top/pointcloud	입력	Lidar에서 나오는 원본 PointCloud2
  pct/point_cloud	출력	Draco 압축 후 전송되는 PointCloud2
  
파라미터	설명

  in_transport	입력 데이터 타입 (raw / draco 등)
  out_transport	출력 데이터 타입 (raw / draco 등)

3. 압축 해제 및 동적 설정

rqt → Plugin → configuration → Dynamic Reconfigure


![draco_plugin](https://github.com/user-attachments/assets/fc325915-9bb8-4f5a-802c-1a009c3da13f)


Draco 압축 해제 파라미터 실시간 조정 가능




4. 구독자 노드 실행
ros2 run point_cloud_transport_tutorial subscriber_test


압축 해제된 데이터를 구독하여 확인

5. SLAMToolbox 사용 시 (3D → 2D 변환)
ros2 run pointcloud_to_laserscan pointcloud_to_laserscan_node --ros-args \
  -r cloud_in:=/out/draco/decompressed \
  -r scan:=/scan \
  -p target_frame:=base_link \
  -p transform_tolerance:=0.01 \
  -p min_height:=0.0 \
  -p max_height:=2.0 \
  -p angle_min:=-3.14 \
  -p angle_max:=3.14 \
  -p angle_increment:=0.0087 \
  -p range_min:=0.1 \
  -p range_max:=50.0 \
  -p qos_overrides./cloud_in.subscription.reliability:=reliable \
  -p qos_overrides./scan.publisher.reliability:=best_effort


3D PointCloud2 → 2D LaserScan 변환

SLAMToolbox 연동 가능 ( ros2 launch slampibot_gazebo spb_slamtoolbox.launch.py

🔧 시스템 구조
[ LiDAR Sensor ]
       │
       ▼
[ /sensing/lidar/top/pointcloud ] (raw)
       │
       ▼
[ Draco Republish Node ]
       │
       ▼
[ pct/point_cloud ] (draco : rqt dynamic reconfigure) 
       │
       ▼
[ Draco Decompress Node / Subscriber ]
       │
       ▼
[ /out/draco/decompressed ] (raw)
       │
       ▼
[ pointcloud_to_laserscan_node ]
       │
       ▼
[ /scan ] (2D LaserScan → SLAMToolbox)

🔧 주요 기능

Draco 압축: PointCloud2 메시지를 효율적으로 압축

저대역폭 전송: 네트워크 전송 최적화

실시간 처리: 센서 데이터를 실시간 처리

확장성: 다양한 센서와 환경에 맞게 확장 가능

📊 시각화 예시
![Visualization_3D_](https://github.com/user-attachments/assets/5b137056-bf18-41c9-ac1e-e78524877e41)![map_12](https://github.com/user-attachments/assets/2112ea18-0273-49f1-b10f-23645c0c7073)

📄 참고자료 


https://github.com/ros-perception/point_cloud_transport_tutorial.git
https://github.com/ros-perception/pointcloud_to_laserscan.git
https://github.com/ros-perception/point_cloud_transport.git
https://github.com/ros-perception/point_cloud_transport_plugins.git
# 3draco
