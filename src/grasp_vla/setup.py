from setuptools import find_packages, setup
import os
from glob import glob

package_name = "grasp_vla"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages",
            ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"),
            glob("launch/*.py")),
        (os.path.join("share", package_name, "config"),
            glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="jeongwon",
    maintainer_email="jeongwonkwak17@gmail.com",
    description="VLA-based grasping pipeline",
    license="MIT",
    entry_points={
        "console_scripts": [
            "grasp_pipeline_node = grasp_vla.grasp_pipeline:main",
        ],
    },
)
