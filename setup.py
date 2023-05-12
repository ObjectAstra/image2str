from distutils.core import setup
setup(
    name = 'image2str',
    packages = ['image2str'],
    version = '1.0.2',
    license = 'MIT',
    description = 'Transform image to ansi string',
    download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords = ['img', 'image', 'terminal', 'show image on terminal', 'ansi', 'ANSI'],
    install_requires=[
            'opencv-python',
            'numpy'
        ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',   
        'Programming Language :: Python :: 3.11', 
    ],
)
