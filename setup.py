"""setuptools based setup script for Bicodon.
This uses setuptools which is now the standard python mechanism for
installing packages. If you have downloaded and uncompressed the
Bicodon source code, or fetched it from git, for the simplest
installation just type the command::
    python setup.py install
However, you would normally install the latest Bicodon release from
the PyPI archive with::
    pip install bicodon
For more in-depth instructions, see the installation section of the
Bicodon manual, linked to from:
https://github.com/laguer/bicodon/wiki/Documentation
Or, if all else fails, feel free to write to the sign up to the Bicodon
mailing list and ask for help.  See:
http://biopython.org/wiki/Mailing_lists
"""
from __future__ import print_function

import sys
import os

try:
    from setuptools import setup
    from setuptools import Command
    from setuptools.command.install import install
    from setuptools.command.build_py import build_py
    from setuptools.command.build_ext import build_ext
    from setuptools import Extension
except ImportError:
    sys.exit(
        "We need the Python library setuptools to be installed. "
        "Try runnning: python -m ensurepip"
    )

if "bdist_wheel" in sys.argv:
    try:
        import wheel  # noqa: F401
    except ImportError:
        sys.exit(
            "We need both setuptools AND wheel packages installed "
            "for bdist_wheel to work. Try running: pip install wheel"
        )

_CHECKED = None


def osx_clang_fix():
    """Add clang switch to ignore unused arguments to avoid OS X compile error.
    This is a hack to cope with Apple shipping a version of Python compiled
    with the -mno-fused-madd argument which clang from XCode 5.1 does not
    support::
        $ cc -v
        Apple LLVM version 5.1 (clang-503.0.40) (based on LLVM 3.4svn)
        Target: x86_64-apple-darwin13.2.0
        Thread model: posix
        $ which python-config
        /Library/Frameworks/Python.framework/Versions/Current/bin/python-config
        $ python-config --cflags
        -I/Library/Frameworks/Python.framework/Versions/2.5/include/python2.5
        -I/Library/Frameworks/Python.framework/Versions/2.5/include/python2.5
        -arch ppc -arch i386 -isysroot /Developer/SDKs/MacOSX10.4u.sdk
        -fno-strict-aliasing -Wno-long-double -no-cpp-precomp -mno-fused-madd
        -fno-common -dynamic -DNDEBUG -g -O3
    We can avoid the clang compilation error with -Qunused-arguments which is
    (currently) harmless if gcc is being used instead (e.g. compiling Biopython
    against a locally compiled Python rather than the Apple provided Python).
    """
    # see http://lists.open-bio.org/pipermail/biopython-dev/2014-April/011240.html
    if sys.platform != "darwin":
        return
    # see also Bicodon/_py3k/__init__.py (which we can't use in setup.py)
    if sys.version_info[0] >= 3:
        from subprocess import getoutput
    else:
        from commands import getoutput
    from distutils.ccompiler import new_compiler
    from distutils.sysconfig import customize_compiler

    # The compiler test should be made on the actual compiler that'll be used
    compiler = new_compiler()
    customize_compiler(compiler)
    cc = getoutput("{} -v".format(compiler.compiler[0]))
    if "gcc" in cc or "clang" not in cc:
        return
    for flag in ["CFLAGS", "CPPFLAGS"]:
        if flag not in os.environ:
            os.environ[flag] = "-Qunused-arguments"
        elif "-Qunused-arguments" not in os.environ[flag]:
            os.environ[flag] += " -Qunused-arguments"


osx_clang_fix()


def is_pypy():
    """Check if running under the PyPy implementation of Python."""
    import platform

    try:
        if platform.python_implementation() == "PyPy":
            return True
    except AttributeError:
        # New in Python 2.6
        pass
    return False


def is_jython():
    """Check if running under the Jython implementation of Python."""
    import platform

    try:
        if platform.python_implementation() == "Jython":
            return True
    except AttributeError:
        # This was missing prior to ~ Jython 2.7.0
        pass
    # Fall back which will work with older Jython:
    return os.name == "java"


def is_ironpython():
    """Check if running under the IronPython implementation of Python."""
    return sys.platform == "cli"
    # TODO - Use platform as in Pypy test?


# Make sure we have the right Python version.
if sys.version_info[:2] < (2, 7):
    sys.stderr.write(
        "Bicodon requires Python 2.7, or Python 3.5 or later. "
        "Python %d.%d detected.\n" % sys.version_info[:2]
    )
    sys.exit(1)
elif sys.version_info[0] < 3:
    sys.stderr.write(
        "=" * 66
        + "\nWARNING: Bicodon will drop support for Python 2.7 in early 2020.\n"
        + "=" * 66
        + "\n"
    )
elif sys.version_info[0] == 3 and sys.version_info[:2] < (3, 5):
    sys.stderr.write(
        "Bicodon requires Python 3.5 or later (or Python 2.7). "
        "Python %d.%d detected.\n" % sys.version_info[:2]
    )
    sys.exit(1)
# if sys.version_info[:2] == (3, 5):
#     print("WARNING: Bicodon support for Python 3.5 is now deprecated.")

if is_jython():
    sys.stderr.write("WARNING: Bicodon support for Jython is now deprecated.\n")


def check_dependencies_once():
    """Check dependencies, will cache and re-use the result."""
    # Call check_dependencies, but cache the result for subsequent
    # calls.
    global _CHECKED
    if _CHECKED is None:
        _CHECKED = check_dependencies()
    return _CHECKED


def check_dependencies():
    """Return whether the installation should continue."""
    # There should be some way for the user to tell specify not to
    # check dependencies.  For example, it probably should not if
    # the user specified "-q".  However, I'm not sure where
    # distutils stores that information.  Also, install has a
    # --force option that gets saved in self.user_options.  It
    # means overwrite previous installations.  If the user has
    # forced an installation, should we also ignore dependencies?

    # Currently there are no compile time dependencies
    return True


class install_bicodon(install):
    """Override the standard install to check for dependencies.
    This will just run the normal install, and then print warning messages
    if packages are missing.
    """

    def run(self):
        """Run the installation."""
        if check_dependencies_once():
            # Run the normal install.
            install.run(self)
        if sys.version_info[0] < 3:
            sys.stderr.write(
                "=" * 66
                + "\nWARNING: Bicodon will drop support for Python 2.7 in early 2020.\n"
                + "=" * 66
                + "\n"
            )


class build_py_bicodon(build_py):
    """Bicodon builder."""

    def run(self):
        """Run the build."""
        if not check_dependencies_once():
            return
        
        # Add software that requires Numpy to be installed.
        if is_jython() or is_ironpython():
            pass
        else:
            self.packages.extend(NUMPY_PACKAGES)
        build_py.run(self)


class build_ext_bicodon(build_ext):
    """Bicodon extension builder."""

    def run(self):
        """Run the build."""
        if not check_dependencies_once():
            return
        build_ext.run(self)


class test_bicodon(Command):
    """Run all of the tests for the package.
    This is a automatic test run class to make distutils kind of act like
    perl. With this you can do:
    python setup.py build
    python setup.py install
    python setup.py test
    """

    description = "Automatically run the test suite for Bicodon."
    user_options = [("offline", None, "Don't run online tests")]

    def initialize_options(self):
        """No-op, initialise options."""
        self.offline = None

    def finalize_options(self):
        """No-op, finalise options."""
        pass

    def run(self):
        """Run the tests."""
        this_dir = os.getcwd()

        # change to the test dir and run the tests
        os.chdir("Tests")
        sys.path.insert(0, "")
        import run_tests

        if self.offline:
            run_tests.main(["--offline"])
        else:
            run_tests.main([])

        # change back to the current directory
        os.chdir(this_dir)


def can_import(module_name):
    """Check we can import the requested module."""
    try:
        return __import__(module_name)
    except ImportError:
        return None


# Using requirements.txt is preferred for an application
# (and likely will pin specific version numbers), using
# setup.py's install_requires is preferred for a library
# (and should try not to be overly narrow with versions).
REQUIRES = ["numpy"]

if is_jython() or is_ironpython():
    REQUIRES.remove("numpy")


# --- set up the packages we are going to install
# standard Bicodon packages

# We now define the Bicodon version number in Bicodon/__init__.py
# Here we can't use "import Bicodon" then "Bicodon.__version__" as that would
# tell us the version of Bicodon already installed (if any).
__version__ = "Undefined"
for line in open("Bicodon/__init__.py"):
    if line.startswith("__version__"):
        exec(line.strip())

# We now load in our reStructuredText README.rst file to pass
# explicitly in the metadata since at time of writing PyPI
# did not do this for us.
#
# Without declaring an encoding, if there was a problematic
# character in the file, it would work on Python 2 but might
# fail on Python 3 depending on the user's locale. By explicitly
# checking ASCII (could use latin1 or UTF8 if needed later),
# if any invalid character does appear in our README, this will
# fail and alert us immediately on either platform.
with open("README.rst", "rb") as handle:
    # Only Python 3's open has an encoding argument.
    # Opening in binary and doing decoding like this to work
    # on both Python 2 and 3.
    readme_rst = handle.read().decode("ascii")

setup(
    name="bicodon",
    version=__version__,
    author="The Bicodon Contributors",
    #author_email="bicodon@",
    url="https://github.com/laguer/Bicodon",
    description="Freely available tools for computational molecular biology.",
    long_description=readme_rst,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: Freely Distributable",
        # Technically the "Bicodon License Agreement" is not OSI approved,
        # but is almost https://opensource.org/licenses/HPND so might put:
        # 'License :: OSI Approved',
        # To resolve this we are moving to dual-licensing with 3-clause BSD:
        # 'License :: OSI Approved :: BSD License',
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    cmdclass={
        "install": install_bicodon,
        "build_py": build_py_bicodon,
        "build_ext": build_ext_bicodon,
        "test": test_bicodon,
    },
    #packages=PACKAGES,
    ext_modules=EXTENSIONS,
    include_package_data=True,  # done via MANIFEST.in under setuptools
    install_requires=REQUIRES,
)
