from setuptools import setup, find_packages

setup(
    name="screen_sharing_app",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyGObject==3.40.1",
        "imageio==2.9.0",
        "aiortc==1.1.2",
        "PyQt5==5.15.4",
        "numpy==1.22.0",
    ],
    entry_points={
        "console_scripts": [
            "screen_sharing_app=main:main",
        ],
    },
    author="Masita",
    description="Aplicación para compartir la pantalla en Ubuntu 24.04 con GNOME",
    license="MIT",
)
