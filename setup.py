# coding = utf-8
from setuptools import setup, find_packages
from geeker import __Version__

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='geeker',
    version=__Version__,
    description=(
        "Many useful functions !"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='liuyalong',
    author_email='4379711@qq.com',
    maintainer='liuyalong',
    maintainer_email='4379711@qq.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/4379711/functools_lyl',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ],
    # 指定入口
    entry_points={
        # 添加命令行脚本
        'console_scripts': [
            'geeker=geeker.cmdline:execute'
        ],
    },

    install_requires=['colorama',
                      'click',
                      'requests',
                      'pandas',
                      'psutil'
                      ]
)
# pip install wheel
# pip install twine

# python setup.py check                 检查错误
# python setup.py sdist bdist_wheel     编译一个tar.gz包,一个wheel包
# twine upload dist/*                   上传到pypi
