from pprint import pprint
import unittest

from nova.objects.instance_numa import InstanceNUMACell
from oslo_versionedobjects.base import VersionedObject,VersionedObjectRegistry
from oslo_versionedobjects.fields import IntegerField, StringField


# TODO(huaqiang): VersionedObject descendent must override the function 'obj_load_attr'?
# TODO(huaqiang): What's the impact of the 'property' statement defined in
#                 oslo_versionedobjects.base._make_class_properties
@VersionedObjectRegistry.register
class FieldClass(VersionedObject):
    """ Target test class

    OVO register: Function will create most properties of target class.
    """
    fields = {
        "count": IntegerField(),
        "name": StringField(),
    }

    def __init__(self):
        pprint(dir(self))
        super(FieldClass, self).__init__()

    # NOTE(huaqiang):
    # VersionedObjectRegistry.register method converts the registering class 'field'
    # items as its properties with the customized property functions.
    # After register OP, class has two kinds of property, the ones has the same name
    # of 'field' items, and the ones left.
    def __setattr__(self, key, value):
        print("[{_class}] __setattr__ called, key={key}, value={value}".format(
            _class=self.__class__.__name__, key=key, value=value
        ))
        if self.__class__.__name__ == 'FieldClass':
            super(FieldClass, self).__setattr__(key, value)
        else:
            setattr(self, key, value)

    def __getattr__(self, item):
        print("[{}] __getattr__ called, key={}".format(self.__class__.__name__, item))
        print(super(FieldClass, self).__dict__)
        print(self.__dict__)
        print()
        if self.__class__.__name__ == 'FieldClass':
            # if support(FieldClass,self).__init__ is not called, then '_changed_fileds'
            # property will not be created.
            getattr(super(FieldClass, self), item)
        else:
            getattr(self, item)


class TestField(unittest.TestCase):
    def test_field_no_default_field_as_attribute(self):
        """ Normally, in a 'ovo.base.VersionedObject' derived class object, there
        is an attribute with the same name of the item of its 'field' element in
        the object, but it not always have such kind of attribute in the object.

        This test is verifying this scenario, that a 'field' item is defined but
        no object attribute existing.
        """
        def _access_name(fieldclass):
            # This function will call FieldClass.__getattr__ method and the
            # 'getter' function registered through 'property' statement.[1]
            # [1] venv/Lib/site-packages/oslo_versionedobjects/base.py:96
            print(fieldclass.name)

        testClass = FieldClass()
        # property 'name' is defined but need to be defined further with 'obj_get_attr'
        self.assertRaises(NotImplementedError, _access_name, testClass)

    def test_field_set_arbitrary_attribute(self):
        """ OVO class also accepts arbitrary attribute other than the fields defined in
        field.

        Class object could easily define an attribute through a simple assignment. Since
        the OVO defined rich field types, how to apply the limit imposed by the field type
        objects. This is not clear for now."""

        def _access_fake(fieldclass):
            return fieldclass.fake

        testClass = FieldClass()
        testClass.fake = 100
        # !!
        # Why VersionedObject is easy to accept the definition of
        # an attribute?
        self.assertEqual(100, _access_fake(testClass))
        print(testClass.obj_fields)
        print(testClass.obj_extra_fields)
        # But 'fake' attribute is not *'in'* the FieldClass
        self.assertFalse('fake' in testClass)
        # NOTE(huaqiang): the *in* OP called the 'hasattr' for the property.
        # field items will register another internal property prefixed with '_obj_',
        # e.g. field {'count': IntegerField} corresponds to '_obj_count',
        # this internal property is not defined by default. Requires to be created
        # with 'property.setter'[1] method.
        # [1] venv/Lib/site-packages/oslo_versionedobjects/base.py:64
        self.assertFalse('count' in testClass)
        testClass.count = 1
        self.assertTrue('count' in testClass)

    def test_nova_instancenumacell_undefine_error(self):
        numacell = InstanceNUMACell(id=0)
        def _access_cpuset(numacell):
            print(numacell.cpuset)
        # NOTE(huaqiang): In class 'InstanceNUMACell', the obj_load_attr method
        # is not overridden also. For any property not calling its @property.setter
        # method returns a 'NotImplementedError'.
        self.assertRaises(NotImplementedError, _access_cpuset, numacell)
