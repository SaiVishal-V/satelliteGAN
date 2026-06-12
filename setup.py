import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="DINCAE", # Replace with your own username
    version="1.1.0",
    author="Alexander Barth",
    description="DINCAE (Data-Interpolating Convolutional Auto-Encoder) is a neural network to reconstruct missing data in satellite observations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gher-ulg/DINCAE",
    packages=setuptools.find_packages(),
    install_requires=[
        "netCDF4>=1.4.2",
        "numpy>=1.16.0",
        "tensorflow>=2.13.0",  # Latest stable version
    ],
    extras_require= {
        "test": [ "pytest-cov",
                  "codecov",
                  "pytest",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license_files=["LICENSE.md"],
)
