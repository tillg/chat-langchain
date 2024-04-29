import json
import logging


def robust_jsonify(obj, *args, **kwargs):

    seen = set()

    class RobustEncoder(json.JSONEncoder):
        def default(self, o):
            """
            Default JSON serializer.
            """
            logger = logging.getLogger(__name__)
            #logger.info(f"Jsonifying {o} with type {type(o)} id: {id(o)}")

            # Take care of circular references
            if id(o) in seen:
                #logger.info(f"Object in seen, returning <Circular Reference>")
                return '<Circular Reference>'
            # Otherwise, add it to the set of seen objects
            seen.add(id(o))

            try:
                # Try to get a dictionary representation of the object
                dict_representation = o.__dict__
                #logger.info(f"Returning dictionary {dict_representation}")
                return dict_representation
            except AttributeError:
                logger.warning(
                    f"Failed to get dictionary representation of {o}")

                # If that fails, convert the object to a string
                try:
                    str = str(o)
                    #logger.info(f"Returning string {str}")
                    return str
                except:
                    logger.warning(f"Failed to convert {o} to string")
                    # If that fails, return the repr of the object
                    return repr(o)

        def encode(self, obj):
            logger = logging.getLogger(__name__)
            #logger.info(f"Encoding {obj} with type {type(obj)} and id {id(obj)}")
            return super().encode(obj)

        def iterencode(self, obj, _one_shot=False):
            logger = logging.getLogger(__name__)
            #logger.info(f"{obj=}, {_one_shot=}")
            iter = super().iterencode(obj, _one_shot)
            #logger.info(f"{iter=}")
            return iter

    logger = logging.getLogger(__name__)
    #logger.info(f"{obj=}, {args=}, {kwargs=}")
    kwargs.setdefault('indent', 3)
    kwargs.setdefault('sort_keys', True)
    kwargs.setdefault('skipkeys', True)
    kwargs.setdefault('cls', RobustEncoder)
    kwargs.setdefault('check_circular', False)
    #logger.info(f"{kwargs=}")

    return json.dumps(obj, *args, **kwargs)
