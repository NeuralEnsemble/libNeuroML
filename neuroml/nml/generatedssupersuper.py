#!/usr/bin/env python3
"""
Super class for GeneratedsSuper

File: neuroml/nml/generatedssupersuper.py

Copyright 2023 NeuroML contributors
"""

import logging
import sys

import neuroml.build_time_validation

from .generatedscollector import GdsCollector

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class GeneratedsSuperSuper(object):
    """Super class for GeneratedsSuper.

    Any bits that must go into every libNeuroML class should go here.
    """

    def add(self, obj=None, hint=None, force=False, validate=True, **kwargs):
        """Generic function to allow easy addition of a new member to a NeuroML object.
        Without arguments, when `obj=None`, it simply calls the `info()` method
        to provide the list of valid member types for the NeuroML class.

        Please use the `info()` method directly for more information on the
        current contents of this component object.

        When `obj` is given a string name of a NeuroML class
        ("NeuroMLDocument"), or the class itself (neuroml.NeuroMLDocument), a
        new object will be created of this type and added as a member to the
        calling (parent) component type object.

        :param obj: member object or class type (neuroml.NeuroMLDocument) or
            name of class type ("NeuroMLDocument"), or None
        :type obj: str or type or None
        :param hint: member name to add to when there are multiple members that `obj` can be added to
        :type hint: string
        :param force: boolean to force addition when an obj has already been added previously
        :type force: bool
        :param validate: validate component after adding (default: True)
        :type validate: bool
        :returns obj: the provided or created object
        :type obj: Object

        :raises Exception: if a member compatible to obj could not be found
        :raises Exception: if multiple members can accept the object and no hint is provided.
        """
        if not obj:
            self.info()
            return
        # a component type has been passed, create and add a new one
        if type(obj) is type or isinstance(obj, str):
            obj = self.component_factory(obj, validate=validate, **kwargs)

        # getattr only returns the value of the provided member but one cannot
        # then use this to modify the member. Using `vars` also allows us to
        # modify the value
        targets = []
        all_members = self._get_members()
        for member in all_members:
            # get_data_type() returns the type as a string, e.g.: 'IncludeType'
            if member.get_data_type() == type(obj).__name__:
                targets.append(member)

        if len(targets) == 0:
            # no targets found
            e = Exception(
                """A member object of {} type could not be found in NeuroML class {}.\n{}
            """.format(type(obj).__name__, type(self).__name__, self.info())
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

        if neuroml.build_time_validation.ENABLED and validate:
            self.validate()
        else:
            logger.warn("Build time validation is disabled.")
        return obj

    @classmethod
    def component_factory(cls, component_type, validate=True, **kwargs):
        """Factory function to create a NeuroML Component object.

        Users can provide the name of the component as a string or the class
        variable, along with its named constructor arguments, and this function
        will create a new object of the Component and return it.

        Users can use the `add()` helper function to further modify components

        This factory runs two checks while creating the component object:

        - that all arguments given do belong to the ComponentType (useful for
          caching typos)
        - that the created component is valid NeuroML

        It is therefore less error prone than creating Components directly using
        the ComponentType constructors.

        It may be useful to disable validation when starting a model. The `validate`
        parameter can be set to False for this.

        :param component_type: component type to create component from:
            this can either be the name of the component as a string, e.g.
            "NeuroMLDocument", or it can be the class type itself: NeuroMLDocument.
            Note that when providing the class type, one will need to import it,
            e.g.: `import NeuroMLDocument`, to ensure that it is defined, whereas
            this will not be required when using the string.
        :type component_type: str/type
        :param validate: toggle validation (default: True)
        :type validate: bool
        :param kwargs: named arguments to be passed to ComponentType constructor
        :type kwargs: named arguments
        :returns: new Component (object) of provided ComponentType
        :rtype: object
        :raises ValueError: if validation/checks fail

        """
        module_object = sys.modules[cls.__module__]

        if isinstance(component_type, str):
            comp_type_class = getattr(module_object, component_type)
        else:
            comp_type_class = getattr(module_object, component_type.__name__)

        comp = comp_type_class(**kwargs)

        # additional setups where required
        if comp_type_class.__name__ == "Cell":
            comp.setup_nml_cell()

        comp._check_arg_list(**kwargs)

        if neuroml.build_time_validation.ENABLED and validate:
            comp.validate()
        else:
            logger.warn("Build time validation is disabled.")
        return comp

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
            if force:
                vars(self)[member.get_name()].append(obj)
            else:
                # "obj in .." checks by identity and value.
                # In XML, two children with same values are identical.
                # There is no use case where the same child would be added
                # twice to a component.
                if obj in vars(self)[member.get_name()]:
                    warnings.warn(
                        """{} already exists in {}. Use `force=True` to force readdition. Hint: you can make changes to the already added object as required without needing to re-add it because only references to the objects are added, not their values.""".format(
                            obj, member.get_name()
                        )
                    )
                else:
                    vars(self)[member.get_name()].append(obj)

    @classmethod
    def _get_members(cls):
        """Get member data items, also from ancestors.

        This function is required because generateDS does not include inherited
        members in the member_data_items list for a derived class. So, for
        example, while IonChannelHH has `gate_hh_rates` which it inherits from
        IonChannel, IonChannelHH's `member_data_items_` is empty. It relies on
        the IonChannel classes' `member_data_items_` list.

        :returns: list of members, including ones inherited from ancestors.
        """
        import copy

        current_class = cls.__name__

        # __all_members_: starting undercores to make it "private", ending
        # underscore to make it match generateds convention where all gds
        # variables have trailing underscores

        # caching: for each class, only get members list the first time
        # `_get_members` is invoked, and store in the dict. For all successive
        # calls, the value is simply returned from the dict. This should not
        # use a lot of memory, and, it'll ensure that repeated calls to
        # `_get_members` are efficient.

        try:
            return cls.__all_members_[current_class]
        # first run
        except AttributeError:
            cls.__all_members_ = {}
        # current class hasn't called it before, so doesn't exist in dict
        except KeyError:
            pass

        # create a copy by value
        # if copied by reference (=), the member_data_items_ object variable is
        # modified to a large list, greatly increasing the memory usage.
        cls.__all_members_[current_class] = copy.copy(cls.member_data_items_)
        for c in cls.__mro__:
            try:
                cls.__all_members_[current_class] += c.member_data_items_
            except AttributeError:
                pass
            except TypeError:
                pass

        cls.__all_members_[current_class] = list(set(cls.__all_members_[current_class]))
        return cls.__all_members_[current_class]

    def info(self, show_contents=False, return_format="string"):
        """Provide information on NeuroML component.


        This is useful to quickly check what members can go into a particular
        NeuroML class (which will match the Schema definitions). It lists these
        members and notes whether they are "single" type elements (Child
        elements) or "List" elements (Children elements). It will also note
        whether a member is optional or required.

        To get a list of possible parents, use the `parentinfo()` method.

        By default, this will only show the members, and not their contents.
        To see contents that have been set, use `show_contents=True`. This will
        not show empty/unset contents. To see all contents, set
        `show_contents=all`.

        Note that not all members will have ids (since not all NeuroML2
        ComponentTypes have ids). For members that do not have ids, the object
        reference is listed instead.

        See http://www.davekuhlman.org/generateDS.html#user-methods for more
        information on the `MemberSpec_` class that generateDS uses.

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

        class_name = self.__class__.__name__
        info_str += f"NeuroMLv2 schema documentation: https://docs.neuroml.org/Userdocs/Schemas/Index.html?highlight={class_name[0].lower()}{class_name[1:]}#{class_name.lower()} for more information.\n\n"
        info_str += "Valid members for {} are:\n".format(class_name)
        all_members = self._get_members()
        for member in all_members:
            info_str += "* {} (class: {}, {})\n".format(
                member.get_name(),
                member.get_data_type(),
                "Optional" if member.get_optional() else "Required",
            )
            if show_contents:
                info_ret[member.get_name()] = {}
                info_ret[member.get_name()]["required"] = (
                    False if member.get_optional() else True
                )
                info_ret[member.get_name()]["type"] = member.get_data_type()
                # Some classes like Annotation can hold anything, and are
                # marked by an __ANY__ member, but a corresponding variable
                # storing contents does not exist. For them, silently return
                # None
                contents = getattr(self, member.get_name(), None)
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
                info_ret[member.get_name()]["members"] = getattr(
                    self, member.get_name(), None
                )
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

    def validate(self, recursive=False):
        """Validate the component.

        Throws a Python `ValueError` if a the component is invalid. You can
        ignore this by using a `try .. except ValueError: pass` block.

        Note: validating your NeuroML file against the schema, which pynml and
        jnml do, will also check this.

        Note: that this is different from the `validate_` method, which does not
        validate inherited members.

        :param recursive: toggle recursive validation (default: False)
        :type recursive: bool
        :returns: None
        :rtype: None
        :raises ValueError: if component is invalid
        """
        collector = GdsCollector()  # noqa
        valid = True
        for c in type(self).__mro__:
            if getattr(c, "validate_", None):
                v = c.validate_(self, collector, recursive)
                valid = valid and v

        if valid is False:
            err = "Validation failed:\n"
            for msg in collector.get_messages():
                err += f"- {msg}\n"
            raise ValueError(err)

    def parentinfo(self, return_format="string"):
        """Show the list of possible parents.

        This object can then be added to objects of the parents using the `add`
        method.

        It is similar to the `info()` method. However, where in the `info()`
        method, it is possible to find the contents of members for a component
        (object) rather easily, it is not so easily possible to get all the
        objects that may refer to another object.

        So, this will provide information on possible parents. It will not
        provide information on whether the components (objects) of the
        particular parent have already been instantiated and what their values
        are. The user should be able to gather this information easily by
        reading the sources.

        Please also note that various component types in NeuroML take ids of
        components as parameters. For example, an `ExplicitInput` will take the
        id of a cell as its `target`, and the id of a `PulseGenerator` as
        `input`. However, these are string fields, and the cell/pulse generator
        classes do not currently know that their ids can be used in
        `ExplicitInput`. This information does not live in the XSD schema, and
        so cannot be obtained here either.

        :param return_format: format in which to return information. If
            "string" (default), an information string is returned. If "list" or
            "dict", a list or dictionary is returned. The list will only
            contain the parent names, whereas the dict will also include
            the member of the parent that the component type matches to.
        :type return_format: str
        :returns: info string, or list of parents or dict with parents as keys
            and member information as values
        :rtype: str, list/dict
        """
        # from nml-core-docs.py in docs
        excluded_classes = [
            "GDSParseError",
            "MixedContainer",
            "MemberSpec_",
            "BlockTypes",
            "Metric",
            "PlasticityTypes",
            "ZeroOrOne",
            "allowedSpaces",
            "channelTypes",
            "gateTypes",
            "networkTypes",
            "populationTypes",
            "_FixedOffsetTZ",
            "GdsCollector_",
            "GeneratedsSuperSuper",
            "attrgetter",
        ]

        # do not show parameters here, they are indicated by members below
        # some classes may not have doc strings, do nothing if they don't
        try:
            info_str = "{}\n\n".format(
                self.__class__.__doc__.split(":param")[0].strip()
            )
        except AttributeError:
            info_str = ""

        info_str += "Please see the NeuroML standard schema documentation at https://docs.neuroml.org/Userdocs/NeuroMLv2.html for more information.\n\n"
        info_str += "Valid parents for {} are:\n".format(self.__class__.__name__)

        retinfo = {}
        module_object = sys.modules[self.__module__]
        nml_ct_classes = dir(module_object)
        for ac in nml_ct_classes:
            if ac.startswith("_") or ac.endswith("_") or ac in excluded_classes:
                continue
            cc = getattr(module_object, ac, None)
            if type(cc) is type:
                try:
                    cc_members = cc()._get_members()
                    for amember in cc_members:
                        # it's a member with the type matching this class
                        if amember.get_data_type() == self.__class__.__name__:
                            # TODO: or it's a member which takes a component
                            # reference. Only checking by NmlId is too noisy,
                            # so not worth adding at the moment. The
                            # information about what ComponentType ID is valid
                            # for a member is not currently exposed to the XSD
                            # schema, and so not available in nml.py
                            # or (amember.get_data_type() == "NmlId" and amember.get_name() != "id"):
                            if ac not in retinfo:
                                retinfo[ac] = {}

                            required = False if amember.get_optional() else True
                            retinfo[ac][amember.get_name()] = {
                                "required": required,
                                "type": amember.get_data_type(),
                            }
                # for classes that aren't NeuroML classes and so don't have
                # get_members() etc. methods
                except AttributeError:
                    pass

        for parent, members in retinfo.items():
            info_str += f"* {parent}\n"
            for name, info in members.items():
                info_str += "\t* {} (class: {}, {})\n".format(
                    name, info["type"], "Required" if info["required"] else "Optional"
                )
        if return_format == "list":
            return list(retinfo.keys())
        elif return_format == "dict":
            return retinfo

        print(info_str)
        return info_str

    def _check_arg_list(self, **kwargs):
        """Check that the correct arguments have been passed for creation of a
        particular Component comp.

        This is required because generally, in Python, if one passes a keyword
        argument that is not listed in a Class constructor, Python will error.
        However, in libNeuroML/nml.py, all constructors have a last keyword
        argument `**kwargs` which means extra keyword arguments that do not match
        the members are silently accepted and then ignored---because they are not
        used in the constructor.

        This means that common mistakes like typos will not be caught by Python,
        and in larger models, one will have to inspect the model in great detail to
        realise that a mistake has been made while creating a component from a
        NeuroML ComponentType.

        This function makes this check manually.

        :param kwargs: arg list passed for creation of component
        :type kwargs: Any
        :returns: None
        :rtype: None
        :raises ValueError: if given argument list does not match permitted  member

        """
        members = self._get_members()
        member_names = []
        for m in members:
            member_names.append(m.get_name())

        args = list(kwargs.keys())

        for arg in args:
            if arg not in member_names:
                err = f"'{arg}' is not a permitted argument for ComponentType '{self.__class__.__name__}'\n"
                print(err)
                self.info()
                raise ValueError(err)

    @classmethod
    def get_class_hierarchy(cls):
        """Get the class hierarchy for a component classs.

        Reference: https://stackoverflow.com/a/75161393/375067

        See the methods in neuroml.utils to use this generated hierarchy.

        :returns: nested single key dictionaries where the key of each
            dictionary is the root node of that subtree, and keys are its
            immediate descendents

        """
        # classes that don't have any members, like ZeroOrNone, which is an Enum
        schema = sys.modules[cls.__module__]
        try:
            allmembers = cls._get_members()
        except AttributeError:
            return {cls.__name__: []}

        retlist = []
        for member in allmembers:
            if member is not None:
                # is it a complex type, which will have a corresponding class?
                member_class = getattr(schema, member.get_data_type(), None)
                # if it isn't a class, so a simple type, just added it with an
                # empty list
                if member_class is None:
                    retlist.append({member.get_name(): []})
                else:
                    # if it is a class, see if it has a hierarchy
                    try:
                        retlist.append(member_class.get_class_hierarchy())
                    except AttributeError:
                        retlist.append({member_class.__name__: []})

        return {cls.__name__: retlist}

    @classmethod
    def get_nml2_class_hierarchy(cls):
        """Return the NeuroML class hierarchy.

        The root here is NeuroMLDocument.
        This is useful in calculating paths to different components to aid in
        construction of relative paths.

        This caches the value as a class variable so that it is not
        re-calculated when used multiple times.
        """
        # if hierarchy exists, return
        try:
            return cls.__nml_hier
        # first run
        except AttributeError:
            schema = sys.modules[cls.__module__]
            cls.__nml_hier = schema.NeuroMLDocument.get_class_hierarchy()
        return cls.__nml_hier
