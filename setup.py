# coding = utf-8
from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='functools_lyl',  # '库的名称,一般写成文件夹的名字就可以了
    version="0.1.0",  # 版本，每次发版本都不能重复，每次发版必须改这个地方
    description=(
        'Some very useful tools'  # 一个简介，别人搜索包时候，这个概要信息会显示在在搜索列表中
    ),
    long_description=long_description,  # 这是详细的，一般是交别人怎么用，很多包没写，那么在官网就造成没有使用介绍了
    long_description_content_type="text/markdown",
    author='liuyalong',  # 作者
    author_email='4379711@qq.com',
    # maintainer='liuyalong',     # 主要的工作人员
    # maintainer_email='4379711@qq.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='http://yalong.site',  # 这个是连接，一般写github就可以了，会从pypi跳转到这里去
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[  # 这里是依赖列表，表示运行这个包的运行某些功能还需要你安装其他的包

    ]
)

# python setup.py check 检查错误
# python setup.py sdist upload -r pypi  上传到pypi

