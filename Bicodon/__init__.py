#
# This file is part of the Bicodon distribution and governed by your
# choice of the "Bicodon License Agreement" or the "BSD 3-Clause License".
# Please see the LICENSE file that should have been included as part of this
# package.
"""Collection of modules for dealing with bicodon data in Python.

The Bicodon Project is an international association of developers
of freely available Python tools for computational molecular biogenetics.

http://github.com/laguer/bicodon
"""

import os
import warnings

__version__ = "1.01.Rev1"


class MissingExternalDependencyError(Exception):
    """Missing an external dependency.

    Used for things like missing command line tools. Important for our unit
    tests to allow skipping tests with missing external dependencies.
    """

    pass


class MissingPythonDependencyError(MissingExternalDependencyError, ImportError):
    """Missing an external python dependency (subclass of ImportError).

    Used for missing Python modules (rather than just a typical ImportError).
    Important for our unit tests to allow skipping tests with missing external
    python dependencies, while also allowing the exception to be caught as an
    ImportError.
    """

    pass


class BicodonWarning(Warning):
    """Bicodon warning.

    Biopython should use this warning (or subclasses of it), making it easy to
    silence all our warning messages should you wish to:

    >>> import warnings
    >>> from Bicodon import BicodonWarning
    >>> warnings.simplefilter('ignore', BicodonWarning)

    Consult the warnings module documentation for more details.
    """

    pass


class BicodonParserWarning(BicodonWarning):
    """Bicodon parser warning.

    Some in-valid data files cannot be parsed and will trigger an exception.
    Where a reasonable interpretation is possible, Bicodon will issue this
    warning to indicate a potential problem. To silence these warnings, use:

    >>> import warnings
    >>> from Bicodon import BicodonParserWarning
    >>> warnings.simplefilter('ignore', BiopythonParserWarning)

    Consult the warnings module documentation for more details.
    """

    pass


class BicodonDeprecationWarning(BicodonWarning):
    """Bicodon deprecation warning.

    Biopython uses this warning instead of the built in DeprecationWarning
    since those are ignored by default since Python 2.7.

    To silence all our deprecation warning messages, use:

    >>> import warnings
    >>> from Bicodon import BicodonDeprecationWarning
    >>> warnings.simplefilter('ignore', BicodonDeprecationWarning)

    Code marked as deprecated is likely to be removed in a future version
    of Bicodon. To avoid removal of this code, please contact the Bicodon
    developers via the mailing list or GitHub.
    """

    pass


class BicodonExperimentalWarning(BicodonWarning):
    """Bicodon experimental code warning.

    Bicodon uses this warning for experimental code ('alpha' or 'beta'
    level code) which is released as part of the standard releases to mark
    sub-modules or functions for early adopters to test & give feedback.

    Code issuing this warning is likely to change (or even be removed) in
    a subsequent release of Bicodon. Such code should NOT be used for
    production/stable code. It should only be used if:

    - You are running the latest release of Bicodon, or ideally the
      latest code from our repository.
    - You are subscribed to the Bicodon-dev mailing list to provide
      feedback on this code, and to be alerted of changes to it.

    If all goes well, experimental code would be promoted to stable in
    a subsequent release, and this warning removed from it.
    """

    pass


_parent_dir = os.path.dirname(os.path.dirname(__file__))
if os.path.exists(os.path.join(_parent_dir, "setup.py")):
    warnings.warn("You may be importing Bicodon from inside the source tree."
                  " This is bad practice and might lead to downstream issues."
                  " In particular, you might encounter ImportErrors due to"
                  " missing compiled C extensions. We recommend that you"
                  " try running your code from outside the source tree."
                  " If you are outside the source tree then you have a"
                  " setup.py file in an unexpected directory: {}.".
                  format(_parent_dir), BicodonWarning)
