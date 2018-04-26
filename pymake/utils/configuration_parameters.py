"""
pymake
-------------------------------

pymake package

 - E. Marinetto
 - nenetto@gmail.com
"""

mandatory_parameters_pymakefile = ['type-of-project',
                                   'author',
                                   'author-email',
                                   'git-repo',
                                   'project-description',
                                   'project-name',
                                   'project-version-major',
                                   'project-version-minor'
                                   ]

mandatory_parameters_pymakeconfigurefile = mandatory_parameters_pymakefile + \
                                           ['configuration']