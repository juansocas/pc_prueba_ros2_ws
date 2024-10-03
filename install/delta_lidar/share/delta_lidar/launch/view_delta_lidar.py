import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
    # Obtener la ruta al directorio del paquete delta_lidar
    delta_lidar_pkg_dir = get_package_share_directory('delta_lidar')

    # Definir la ruta al archivo delta_lidar.launch
    delta_lidar_launch_file = os.path.join(delta_lidar_pkg_dir, 'launch', 'delta_lidar.launch')

    # Definir un argumento de lanzamiento para los argumentos de RViz
    rviz_args = DeclareLaunchArgument('rviz_args', default_value='-d $(find delta_lidar)/rviz/delta_lidar.rviz',
                                      description='Arguments for RViz')

    # Crear una descripción de lanzamiento que incluya delta_lidar.launch
    delta_lidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(delta_lidar_launch_file)
    )

    # Crear un nodo para RViz
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz',
        output='screen',
        arguments=[LaunchConfiguration('rviz_args')]
    )

    # Devolver la descripción completa del lanzamiento
    return LaunchDescription([
        rviz_args,
        delta_lidar_launch,
        rviz_node
    ])
