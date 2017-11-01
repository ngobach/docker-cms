#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2012 Bernard Blackham <bernard@largestprime.net>
# Copyright © 2013-2015 Stefano Maggiolo <s.maggiolo@gmail.com>
# Copyright © 2014-2015 Giovanni Mascellani <mascellani@poisson.phc.unipi.it>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import cmstestsuite.tasks.batch_stdio as batch_stdio
import cmstestsuite.tasks.batch_fileio as batch_fileio
import cmstestsuite.tasks.batch_fileio_managed as batch_fileio_managed
import cmstestsuite.tasks.communication as communication

from cms import LANGUAGES, LANG_C, LANG_CPP, LANG_PASCAL, LANG_JAVA, \
    LANG_PYTHON
from cmstestsuite.Test import Test, CheckOverallScore, CheckCompilationFail, \
    CheckTimeout, CheckTimeoutWall, CheckNonzeroReturn


ALL_LANGUAGES = tuple(LANGUAGES)
NON_INTERPRETED_LANGUAGES = (LANG_C, LANG_CPP, LANG_PASCAL)
COMPILED_LANGUAGES = (LANG_C, LANG_CPP, LANG_PASCAL, LANG_JAVA, LANG_PYTHON)

ALL_TESTS = [

    # Correct solutions to batch tasks.

    Test('correct-stdio',
         task=batch_stdio, filename='correct-stdio.%l',
         languages=ALL_LANGUAGES,
         checks=[CheckOverallScore(100, 100)]),

    Test('correct-freopen',
         task=batch_fileio, filename='correct-freopen.%l',
         languages=(LANG_C,),
         checks=[CheckOverallScore(100, 100)]),

    Test('correct-fileio',
         task=batch_fileio, filename='correct-fileio.%l',
         languages=ALL_LANGUAGES,
         checks=[CheckOverallScore(100, 100)]),

    # Various incorrect solutions to batch tasks.

    Test('incorrect-stdio',
         task=batch_stdio, filename='incorrect-stdio.%l',
         languages=ALL_LANGUAGES,
         checks=[CheckOverallScore(0, 100)]),

    Test('half-correct-stdio',
         task=batch_stdio, filename='half-correct-stdio.%l',
         languages=ALL_LANGUAGES,
         checks=[CheckOverallScore(50, 100)]),

    Test('incorrect-fileio',
         task=batch_fileio, filename='incorrect-fileio.%l',
         languages=ALL_LANGUAGES,
         checks=[CheckOverallScore(0, 100)]),

    Test('half-correct-fileio',
         task=batch_fileio, filename='half-correct-fileio.%l',
         languages=ALL_LANGUAGES,
         checks=[CheckOverallScore(50, 100)]),

    Test('incorrect-fileio-nooutput',
         task=batch_fileio, filename='incorrect-fileio-nooutput.%l',
         languages=(LANG_C,),
         checks=[CheckOverallScore(0, 100)]),

    Test('incorrect-fileio-emptyoutput',
         task=batch_fileio, filename='incorrect-fileio-emptyoutput.%l',
         languages=(LANG_C,),
         checks=[CheckOverallScore(0, 100)]),

    Test('incorrect-fileio-with-stdio',
         task=batch_fileio, filename='incorrect-fileio-with-stdio.%l',
         languages=ALL_LANGUAGES,
         checks=[CheckOverallScore(0, 100)]),

    # Failed compilation.

    Test('compile-fail',
         task=batch_fileio, filename='compile-fail.%l',
         languages=COMPILED_LANGUAGES,
         checks=[CheckCompilationFail()]),

    # Various timeout conditions.

    Test('timeout-cputime',
         task=batch_stdio, filename='timeout-cputime.%l',
         languages=ALL_LANGUAGES,
         checks=[CheckOverallScore(0, 100), CheckTimeout()]),

    Test('timeout-pause',
         task=batch_stdio, filename='timeout-pause.%l',
         languages=(LANG_CPP,),
         checks=[CheckOverallScore(0, 100), CheckTimeoutWall()]),

    Test('timeout-sleep',
         task=batch_stdio, filename='timeout-sleep.%l',
         languages=(LANG_CPP,),
         checks=[CheckOverallScore(0, 100), CheckTimeout()]),

    Test('timeout-sigstop',
         task=batch_stdio, filename='timeout-sigstop.%l',
         languages=(LANG_CPP,),
         checks=[CheckOverallScore(0, 100), CheckTimeout()]),

    Test('timeout-select',
         task=batch_stdio, filename='timeout-select.%l',
         languages=(LANG_CPP,),
         checks=[CheckOverallScore(0, 100), CheckTimeout()]),

    # Nonzero return status.

    Test('nonzero-return-stdio',
         task=batch_stdio, filename='nonzero-return-stdio.%l',
         languages=ALL_LANGUAGES,
         checks=[CheckOverallScore(0, 100), CheckNonzeroReturn()]),

    Test('nonzero-return-fileio',
         task=batch_fileio, filename='nonzero-return-fileio.%l',
         languages=ALL_LANGUAGES,
         checks=[CheckOverallScore(0, 100), CheckNonzeroReturn()]),

    # Fork

    # We can't really check for a specific error, because forking
    # doesn't cause an exceptional stop: it just returns -1 to the
    # caller; we rely on the fact that the test program is designed to
    # produce output only inside the child process

    Test('fork',
         task=batch_stdio, filename='fork.%l',
         languages=(LANG_C, LANG_CPP),
         checks=[CheckOverallScore(0, 100)]),

    # OOM problems.

    Test('oom-static',
         task=batch_stdio, filename='oom-static.%l',
         languages=NON_INTERPRETED_LANGUAGES,
         checks=[CheckOverallScore(0, 100)]),

    Test('oom-heap',
         task=batch_stdio, filename='oom-heap.%l',
         languages=ALL_LANGUAGES,
         checks=[CheckOverallScore(0, 100)]),

    # Tasks with graders. Python and PHP are not yet supported.

    Test('managed-correct',
         task=batch_fileio_managed, filename='managed-correct.%l',
         languages=(LANG_C, LANG_CPP, LANG_PASCAL, LANG_JAVA),
         checks=[CheckOverallScore(100, 100)]),

    Test('managed-incorrect',
         task=batch_fileio_managed, filename='managed-incorrect.%l',
         languages=(LANG_C, LANG_CPP, LANG_PASCAL, LANG_JAVA),
         checks=[CheckOverallScore(0, 100)]),

    # Communication tasks. Python and PHP are not yet supported.

    Test('communication-correct',
         task=communication, filename='communication-correct.%l',
         languages=(LANG_C, LANG_CPP, LANG_PASCAL, LANG_JAVA),
         checks=[CheckOverallScore(100, 100)]),

    Test('communication-incorrect',
         task=communication, filename='communication-incorrect.%l',
         languages=(LANG_C, LANG_CPP, LANG_PASCAL, LANG_JAVA),
         checks=[CheckOverallScore(0, 100)]),

    # Writing to files not allowed.

    # Inability to write to a file does not throw a specific error,
    # just returns a NULL file handler to the caller. So we rely on
    # the test program to write the correct result only if the
    # returned handler is valid.

    Test('write-forbidden-fileio',
         task=batch_fileio, filename='write-forbidden-fileio.%l',
         languages=(LANG_C),
         checks=[CheckOverallScore(0, 100)]),

    Test('write-forbidden-stdio',
         task=batch_stdio, filename='write-forbidden-stdio.%l',
         languages=(LANG_C),
         checks=[CheckOverallScore(0, 100)]),

    Test('write-forbidden-managed',
         task=batch_fileio_managed, filename='write-forbidden-managed.%l',
         languages=(LANG_C),
         checks=[CheckOverallScore(0, 100)]),

    Test('write-forbidden-communication',
         task=communication, filename='write-forbidden-communication.%l',
         languages=(LANG_C),
         checks=[CheckOverallScore(0, 100)]),

    # This tests complete successfully only if it is unable to execute
    # output.txt.

    Test('executing-output',
         task=batch_fileio, filename='executing-output.%l',
         languages=(LANG_C),
         checks=[CheckOverallScore(100, 100)]),

    # Rewrite input in the solution.

    Test('rewrite-input',
         task=batch_fileio_managed, filename='rewrite-input.%l',
         languages=(LANG_C,),
         checks=[CheckOverallScore(0, 100)]),

    Test('delete-write-input',
         task=batch_fileio_managed, filename='delete-write-input.%l',
         languages=(LANG_C,),
         checks=[CheckOverallScore(0, 100)]),

    # Write a huge file

    Test('write-big-fileio',
         task=batch_fileio, filename='write-big-fileio.%l',
         languages=LANG_C,
         checks=[CheckOverallScore(0, 100)]),

]
