from inspect import stack

from management.logger.logger import Log


class ObjectsManager:

    __objects = {}

    def __init__(self):
        raise NotImplementedError("Cannot Instantiate ObjectsManager!")

    @classmethod
    def get_object_by_name(cls, object_name):

        Log.info(f"Trying to get {object_name} instance...", stack()[1])

        _object = None
        repr_object_name = None

        try:
            repr_object_name = repr(object_name)
            _object = cls.__objects[object_name]

        except KeyError:
            Log.exception(f"{repr_object_name} doesn't exist!", stack()[1])
            return None

        except AttributeError as E:
            Log.exception(f"_object is not a class! - {E}", stack()[1])
            return None

        else:
            Log.debug(f"Found {repr_object_name}", stack()[1])
            return _object

    @classmethod
    def destruct_objects(cls):
        leak_found = False
        Log.debug("Looking for memory leaks!", stack()[1])
        for _object in [*cls.__objects]:
            leak_found = True
            Log.warning(f"Found a memory leak!, object is {_object}", stack()[1])
            del cls.__objects[_object]

        if leak_found:
            Log.warning("Found some leaks but cleaned them up!", stack()[1])

        else:
            Log.info("No leaks found!", stack()[1])

    @classmethod
    def create_object(cls, _object, *args, custom_name=None, **kwargs):

        repr_object_name = None

        try:
            object_name = custom_name if custom_name else _object.__name__
            repr_object_name = f"'{object_name}'"
            cls.__objects[object_name] = _object(*args, **kwargs)

        except AttributeError:
            Log.exception(f"object '{_object}' is not a class!", stack()[1])
            return None

        except Exception as E:
            Log.exception(f"Some Error occurred while creating object {repr_object_name}!{E}", stack()[1])
            return None

        Log.debug(f"Successfully created Object {repr_object_name}!", stack()[1])
        return cls.__objects[object_name]

    @classmethod
    def delete_object(cls, object_name):

        Log.info(f"Trying to delete {object_name} instance...!", stack()[1])
        repr_object_name = repr(object_name)

        try:
            del cls.__objects[object_name]

        except KeyError:
            Log.exception(f"{repr_object_name} doesn't exist!", stack()[1])

        except Exception as E:
            Log.exception(f"Error happened!{E}", stack()[1])

        else:
            Log.debug(f"Successfully deleted {repr_object_name}", stack()[1])
