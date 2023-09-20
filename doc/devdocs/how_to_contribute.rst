How to contribute
=================

libNeuroML development happens on GitHub, so you will need a GitHub account to contribute to the repository.
Contributions are made using the standard `Pull Request`_ workflow.

Setting up
----------

Please take a look at the GitHub documentation here: http://help.github.com/fork-a-repo/

To begin, please fork the repo on the GitHub website.
You should now have a libNeuroML under you username.
Next, we clone our fork to get a local copy on our computer:

::

    git clone git@github.com:_username_/libNeuroML.git

While not necessary, it is good practice to add the upstream repository as a remote that you will follow:

::

    cd libNeuroML
    git remote add upstream https://github.com/NeuralEnsemble/libNeuroML.git
    git fetch upstream


You can check which branch are you following doing:

::

    git branch -a

You should have something like:

::

    git branch -a
    * master
      remotes/origin/HEAD -> origin/master
      remotes/origin/master
      remotes/upstream/master


Sync with upstream
------------------

Before starting to do some work, please check to see that you have the latest copy of the sources in your local repository:

::

    git fetch upstream
    git checkout development
    git merge upstream/development

Working locally on a dedicated branch
-------------------------------------

Now that we have a fork, we can start making our changes to the source code.
The best way to do it is to create a branch with a descriptive name to indicate what are you working on.
Generally, your will branch off from the upstream `development` branch, which will contain the latest code.

For example, just for the sake of this guide, I'm going to work on issue #2.

::

    git checkout development
    git checkout -b fix-2


We can work in this branch, and make as many commits as we need to:

::

    # hack hack hack
    git commit -am "some decent commit message here"


Once we have finished working, we can push the branch online to our fork:

::

   git push origin fix-2


We can then open a pull-request to merge our ``fix-2`` branch into ``upstream/development``.
If your code is not ready to be included, you can update the code on your branch and any more commits you add there will be added to the Pull Request.
Members of the libNeuroML development team will then discuss your changes with you, perhaps suggest tweaks, and then merge it when ready.

Continuous integration
-----------------------

libNeuroML uses continuous integration (`Wikipedia <https://en.wikipedia.org/wiki/Continuous_integration>`_).
Each commit to the master or development branches is tested, along with all commits to pull requests.
The latest status of the continuous integration tests can be seen `here on GitHub Actions <https://github.com/NeuralEnsemble/libNeuroML/actions>`_.

Release process
---------------

libNeuroML is part of the official NeuroML release cycle.
When a new libNeuroML release is ready the following needs to happen:

- Update version number in setup.cfg
- update version number in doc/conf.py
- update release number in doc/conf.py (same as version number)
- update changelog in README.md
- merge development branch with master (This should happen via pull request - do not do the merge yourself even if you are an owner of the repository.
- push latest release to PyPi

More information on the NeuroML release process can be found on the `NeuroML documentation page <https://docs.neuroml.org/Devdocs/ReleaseProcess.html>`_.

.. _Pull Request: http://help.github.com/send-pull-requests/
