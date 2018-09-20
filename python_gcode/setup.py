import setuptools

import versioneer

def read_requirements(path="requirements.txt"):
    def yield_line(path):
        with open(path, "r") as fid:
            for line in fid.readlines():
                yield line

    return [requirement.strip() for requirement in yield_line(path) if not requirement.startswith("#")]

requirements = read_requirements()

setuptools.setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    name="GCode",
    description="GCode",
    author="Jed",
    license="BSD",
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=requirements,
    include_package_data=True,
)
