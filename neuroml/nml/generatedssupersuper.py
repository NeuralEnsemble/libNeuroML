#!/usr/bin/env python3
"""
Super class for GeneratedsSuper

File: neuroml/nml/generatedssupersuper.py

Copyright 2022 NeuroML contributors
"""


from .generatedscollector import GdsCollector


class GeneratedsSuperSuper(object):

    """Super class for GeneratedsSuper.

    Any bits that must go into every libNeuroML class should go here.
    """

    def add(self, obj=None, hint=None, force=False):
        """Generic function to allow easy addition of a new member to a NeuroML object.

        Without arguments, when `obj=None`, it simply calls the `info()` method
        to provide the list of valid member types for the NeuroML class.

        Use `info(show_contents=True)` to see the valid members of this class,
        and their current contents.

        :param obj: object member to add
        :type obj: any NeuroML Type defined by the API
        :param hint: member name to add to when there are multiple members that `obj` can be added to
        :type hint: string
        :param force: boolean to force addition when an obj has already been added previously
        :type force: bool

        :raises Exception: if a member compatible to obj could not be found
        :raises Exception: if multiple members can accept the object and no hint is provided.
        """
        if not obj:
            self.info()
            return

        # getattr only returns the value of the provided member but one cannot
        # then use this to modify the member. Using `vars` also allows us to
        # modify the value
        targets = []
        all_members = self.get_members()
        for member in all_members:
            # get_data_type() returns the type as a string, e.g.: 'IncludeType'
            if member.get_data_type() == type(obj).__name__:
                targets.append(member)

        if len(targets) == 0:
            # no targets found
            e = Exception(
                """A member object of {} type could not be found in NeuroML class {}.\n{}
            """.format(
                    type(obj).__name__, type(self).__name__, self.info()
                )
            )
            raise e
        elif len(targets) == 1:
            # good, just add it
            self.__add(obj, targets[0], force)
        else:
            # more than one target
            if not hint:
                err_string = """Multiple members can accept {}. Please provide the name of the variable using the `hint` argument to specify which member to add to:\n""".format(
                    type(obj).__name__
                )
                for t in targets:
                    err_string += "- {}\n".format(t.get_name())
                raise Exception(err_string)

            # use hint to figure out which target to use
            for t in targets:
                if hint == t.get_name():
                    self.__add(obj, t, force)
                    break

    def __add(self, obj, member, force=False):
        """Private method to add new member to a specified variable in a NeuroML object.

        :param obj: object member to add
        :type obj: any NeuroML Type defined by the API
        :param member: member variable name to add to when there are multiple members that `obj` can be added to
        :type member: MemberSpec_
        :param force: boolean to force addition when an obj has already been added previously
        :type force: bool

        """
        import warnings

        # A single value, not a list:
        if member.get_container() == 0:
            if force:
                vars(self)[member.get_name()] = obj
            else:
                if vars(self)[member.get_name()]:
                    warnings.warn(
                        """{} has already been assigned.  Use `force=True` to overwrite. Hint: you can make changes to the already added object as required without needing to re-add it because only references to the objects are added, not their values.""".format(
                            member.get_name()
                        )
                    )
                else:
                    vars(self)[member.get_name()] = obj
        # List
        else:
            # Do not use 'obj in ..' for membership check because it also
            # returns true if an element with the same value exists in the
            # container
            # https://docs.python.org/3/reference/expressions.html#membership-test-operations
            if force:
                vars(self)[member.get_name()].append(obj)
            else:
                if any(obj is e for e in vars(self)[member.get_name()]):
                    warnings.warn(
                        """{} already exists in {}. Use `force=True` to force readdition. Hint: you can make changes to the already added object as required without needing to re-add it because only references to the objects are added, not their values.""".format(
                            obj, member.get_name()
                        )
                    )
                else:
                    vars(self)[member.get_name()].append(obj)

    def get_members(self):
        """Get member data items, also from ancestors.

        This function is required because generateDS does not include inherited
        members in the member_data_items list for a derived class. So, for
        example, while IonChannelHH has `gate_hh_rates` which it inherits from
        IonChannel, IonChannelHH's `member_data_items_` is empty. It relies on
        the IonChannel classes' `member_data_items_` list.

        :returns: list of members, including ones inherited from ancestors.
        """
        import copy

        # create a copy by value
        # if copied by reference (=), the member_data_items_ object variable is
        # modified to a large list, greatly increasing the memory usage.
        all_members = copy.copy(self.member_data_items_)
        for c in type(self).__mro__:
            try:
                all_members.extend(c.member_data_items_)
            except AttributeError:
                pass
            except TypeError:
                pass

        # deduplicate
        # TODO where are the duplicates coming from given that we're not
        # calling this recursively?
        all_members = list(set(all_members))
        return all_members

    def info(self, show_contents=False, return_format="string"):
        """A helper function to get a list of members of this class.

        This is useful to quickly check what members can go into a particular
        NeuroML class (which will match the Schema definitions). It lists these
        members and notes whether they are "single" type elements (Child
        elements) or "List" elements (Children elements). It will also note
        whether a member is optional or required.

        By default, this will only show the members, and not their contents.
        To see contents that have been set, use `show_contents=True`. This will
        not show empty/unset contents. To see all contents, set
        `show_contents=all`.

        Note that not all members will have ids (since not all NeuroML2
        ComponentTypes have ids). For members that do not have ids, the object
        reference is listed instead.

        See http://www.davekuhlman.org/generateDS.html#user-methods for more
        information on the MemberSpec_ class that generateDS uses.

        :param show_contents: toggle to print out the contents of the members
        :type show_contents: bool or str
        :param return_format: select what format to return information in
            "string" (default), or "dict" or "list".

            If "dict" or "list" is provided, the information is returned as a
            dict/list instead of being printed. Note that if `show_contents` is
            `False`, only a list of members is available and will be returned
            even if "dict" is supplied. If `show_contents` is `True` or "all"
            but "list" is provided, only the list of members will be returned.
            If something other than "string", "list", or "dict" is provided,
            the string representation is returned and printed.
        :type return_format: str
        :returns: info string, or list of members or dict with members as keys
            and member values as values
        :rtype: str, list/dict
        """
        if show_contents:
            info_ret = {}
        else:
            info_ret = []

        # do not show parameters here, they are indicated by members below
        # some classes may not have doc strings, do nothing if they don't
        try:
            info_str = "{}\n\n".format(
                self.__class__.__doc__.split(":param")[0].strip()
            )
        except AttributeError:
            info_str = ""

        info_str += "Please see the NeuroML standard schema documentation at https://docs.neuroml.org/Userdocs/NeuroMLv2.html for more information.\n\n"
        info_str += "Valid members for {} are:\n".format(self.__class__.__name__)
        all_members = self.get_members()
        for member in all_members:
            info_ret[member.get_name()] = {}
            info_str += "* {} (class: {}, {})\n".format(
                member.get_name(),
                member.get_data_type(),
                "Optional" if member.get_optional() else "Required",
            )
            info_ret[member.get_name()]["required"] = False if member.get_optional() else True
            if show_contents:
                contents = getattr(self, member.get_name())
                # check if the member is set to None
                # if it's a container (list), it will not be set to None, it
                # will be empty, []
                # if it's a scalar, it will be set to None or to a non
                # container value
                if contents is None or (
                    isinstance(contents, list) and len(contents) == 0
                ):
                    if show_contents == "all":
                        info_str += "\t* Contents: {}\n\n".format(contents)
                else:
                    contents_id = None
                    # if list, iterate to get ids
                    if isinstance(contents, list):
                        contents_id = []
                        for c in contents:
                            if hasattr(c, "id"):
                                contents_id.append(c.id)
                            else:
                                contents_id.append(c)
                    # not a list, a scalar
                    else:
                        if hasattr(contents, "id"):
                            contents_id = f"'{contents.id}'"
                        else:
                            contents_id = contents
                    info_str += "\t* Contents ('ids'/<objects>): {}\n\n".format(
                        contents_id
                    )
                info_ret[member.get_name()]['members'] = getattr(self, member.get_name())
            else:
                info_ret.append(member.get_name())

        if return_format == "list":
            if isinstance(info_ret, dict):
                return list(info_ret.keys())
            else:
                return info_ret
        elif return_format == "dict":
            return info_ret

        print(info_str)
        return info_str

    def validate(self):
        """Validate the component.

        Throws a Python `ValueError` if a the component is invalid. You can
        ignore this by using a `try .. except ValueError: pass` block.

        Note: validating your NeuroML file will also check this.

        Note: that this is different from the `validate_` method, which does not
        validate inherited members.

        :returns: None
        :rtype: None
        :raises ValueError: if component is invalid
        """
        collector = GdsCollector()  # noqa
        valid = True
        for c in type(self).__mro__:
            if getattr(c, "validate_", None):
                v = c.validate_(self, collector)
                valid = valid and v

        if valid is False:
            err = "Validation failed:\n"
            for msg in collector.get_messages():
                err += f"- {msg}\n"
            raise ValueError(err)
