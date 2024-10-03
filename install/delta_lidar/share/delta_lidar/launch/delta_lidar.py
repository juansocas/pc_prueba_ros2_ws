import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Obtener la ruta al ejecutable delta_lidar_node
    package_name = 'delta_lidar'
    executable = 'delta_lidar_node'
    node_namespace = ''  # Puedes definir un espacio de nombres si es necesario

    # Definir los parámetros serial_port y frame_id
    serial_port_param = {'serial_port': '/dev/ttyUSB0'}
    frame_id_param = {'frame_id': 'laser'}

    # Crear un nodo para el ejecutable delta_lidar_node
    delta_lidar_node = Node(
        package=package_name,
        executable=executable,
        name='delta_lidar',
        namespace=node_namespace,
        output='screen',
        parameters=[serial_port_param, frame_id_param]
    )

    # Devolver la descripción completa del lanzamiento
    return LaunchDescription([delta_lidar_node])