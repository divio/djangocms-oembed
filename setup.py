from setuptools import setup, find_packages

setup(
    name = "djangocms-oembed",
    version = __import__('djangocms_oembed').__version__,
    url = 'http://github.com/divio/djangocms-oembed',
    license = 'BSD',
    platforms=['OS Independent'],
    description = "A set of oembed plugins for django CMS.",
    author = 'Divio AG',
    author_email = 'developers@divio.ch',
    packages=find_packages(),
    install_requires = (
        'Django>=1.4',
        'django-cms',
        'pyquery',
        'micawber',
    ),
    include_package_data=True,
    zip_safe=False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
