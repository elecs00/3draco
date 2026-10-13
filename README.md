# 3draco — Draco 압축을 적용한 3D LiDAR 전송과 2D SLAM (ROS2)

3D LiDAR(Ouster 32채널)의 대용량 PointCloud2 를 Google Draco 로 압축해 전송하고, 압축을 푼 점군으로 2D SLAM 지도를 만드는 ROS2 파이프라인입니다. 압축 품질(양자화 비트)에 따라 **압축률·전송시간·손실률**이 어떻게 바뀌는지 측정했습니다.

| 항목 | 내용 |
|---|---|
| 형태 | 4인 팀 프로젝트 (K-Digital Training, 2025-09-29 ~ 10-20, 3주) |
| **내 역할** | **통합** (압축·해제·변환·SLAM 노드를 하나의 파이프라인으로 연결), **실험** (양자화 비트별 성능 측정), **결과보고서** 작성 |
| 데이터 | Ouster 32채널 rosbag2 (sqlite3, 10Hz, 약 43초, 점군 435개) |
| 사용 기술 | ROS2 Humble, point_cloud_transport + Draco 플러그인, pointcloud_to_laserscan, SLAM Toolbox, rf2o 레이저 오도메트리, Cartographer(3D 시험), RViz2 |

📄 **결과보고서**: [`결과보고서_Draco기술을 이용한 2D SLAM.pdf`](결과보고서_Draco기술을%20이용한%202D%20SLAM.pdf)

## 🔧 파이프라인

```
rosbag2 (/sensing/lidar/top/pointcloud, raw)
   │  point_cloud_transport republish  (raw → draco)
   ▼
/out/draco  (압축 전송, rqt Dynamic Reconfigure 로 양자화 비트 실시간 조정)
   │  my_subscriber  (draco 해제 + 포인트 수 로그)
   ▼
/out/draco/decompressed  (PointCloud2) ──▶ RViz2 시각화
   │  pointcloud_to_laserscan
   ▼
/scan (LaserScan) ──▶ rf2o 레이저 오도메트리 + SLAM Toolbox ──▶ 2D 지도
```

## 📊 실험 결과 (양자화 비트별)

Draco 설정: `encode_speed=1`(압축률 우선), `decode_speed=10`(해제 속도 우선) 고정, `quantization_POSITION` 을 6~18 비트로 바꾸며 측정.

| 양자화 | 결과 |
|---|---|
| 8 bit | 전송이 가장 빠르나 점 손실로 시각 품질 저하 |
| 10 bit | 전송시간 약 170ms, 품질과 속도의 균형이 가장 적절 |
| 12 bit | 품질 가장 높음, 전송시간 200ms 이상으로 실시간성 부족 |

- 결론: 실시간성이 최우선이면 8 bit, 품질·속도 균형은 10 bit.
- 한계(보고서 자체 평가): 전송시간·압축률·대역폭·FPS 를 같은 실행에서 동시에 측정하지 못해 비교가 체계적이지 못했음.

<img src="https://github.com/user-attachments/assets/5b137056-bf18-41c9-ac1e-e78524877e41" alt="압축 해제 점군 시각화" width="480" /> <img src="https://github.com/user-attachments/assets/2112ea18-0273-49f1-b10f-23645c0c7073" alt="2D SLAM 지도" width="320" />

## 🧩 직접 수정·추가한 파일

이 저장소의 대부분은 외부 오픈소스입니다. 팀이 수정하거나 추가한 파일은 아래와 같습니다.

| 파일 | 내용 |
|---|---|
| `draco_ws/src/point_cloud_transport_tutorial/src/my_subscriber.cpp` | draco 전송 지정 구독, 해제된 점군을 `/out/draco/decompressed` 로 재발행(RViz2·SLAM 입력용) |
| `draco_ws/src/point_cloud_transport_tutorial/src/my_publisher.cpp` | rosbag 저장 형식을 `mcap` → `sqlite3` 로 변경 (실험 데이터가 sqlite3 형식) |
| `ros2spb-humble-erail/src/slampibot_gazebo/launch/spb_slamtoolbox.launch.py` | rosbag 재생용(`use_sim_time`), 휠 오도메트리 대신 rf2o 레이저 오도메트리 연결 |
| `ros2spb-humble-erail/src/slampibot_gazebo/params/mapper_params_online_async.yaml` | `base_link` 기준, 지도 갱신 1초, 최소 이동 거리·회전 0.1 로 조정 |
| `ros2spb-humble-erail/src/slampibot_gazebo/launch/spb_cartographer.launch.py`, `params/spb_cartographer_3d_gazebo.lua` | 압축 해제 점군을 입력으로 쓰는 3D Cartographer 시험 설정 |

## 📦 외부 오픈소스

| 폴더 | 원본 |
|---|---|
| `draco_ws/src/point_cloud_transport-humble` | https://github.com/ros-perception/point_cloud_transport (humble) |
| `draco_ws/src/point_cloud_transport_tutorial` | https://github.com/ros-perception/point_cloud_transport_tutorial |
| `ros2spb-humble-erail/src/slampibot_*` | https://github.com/edurobotailab/slampibot-humble-v7 |
| `ros2spb-humble-erail/src/rf2o_laser_odometry` | https://github.com/MAPIRlab/rf2o_laser_odometry |
| (apt) Draco 플러그인 | https://github.com/ros-perception/point_cloud_transport_plugins |
| (apt) pointcloud_to_laserscan | https://github.com/ros-perception/pointcloud_to_laserscan |

## 🛠 설치 및 빌드

```bash
sudo apt install ros-humble-point-cloud-transport \
                 ros-humble-draco-point-cloud-transport \
                 ros-humble-pointcloud-to-laserscan \
                 ros-humble-slam-toolbox
cd draco_ws && colcon build && source install/setup.bash
```

## 💡 실행 순서

1. rosbag 재생
   ```bash
   ros2 bag play <rosbag 폴더> --clock
   ```
2. Draco 압축 재발행 (raw → draco)
   ```bash
   ros2 run point_cloud_transport republish --ros-args \
     -r in:=/sensing/lidar/top/pointcloud -r out:=/out \
     -p in_transport:=raw -p out_transport:=draco
   ```
   > 구독 노드가 `/out` 을 draco 로 구독하므로 출력 이름을 `/out` 으로 맞춥니다.
3. 양자화 비트 조정: `rqt` → Plugins → Configuration → Dynamic Reconfigure
4. 압축 해제 + 재발행
   ```bash
   ros2 run point_cloud_transport_tutorial subscriber_test
   ```
5. 3D → 2D 변환
   ```bash
   ros2 run pointcloud_to_laserscan pointcloud_to_laserscan_node --ros-args \
     -r cloud_in:=/out/draco/decompressed -r scan:=/scan \
     -p target_frame:=base_link -p transform_tolerance:=0.01 \
     -p min_height:=0.0 -p max_height:=2.0 \
     -p angle_min:=-3.14 -p angle_max:=3.14 -p angle_increment:=0.0087 \
     -p range_min:=0.1 -p range_max:=50.0 \
     -p qos_overrides./cloud_in.subscription.reliability:=best_effort \
     -p qos_overrides./scan.publisher.reliability:=best_effort
   ```
6. SLAM
   ```bash
   ros2 launch slampibot_gazebo spb_slamtoolbox.launch.py
   ```
