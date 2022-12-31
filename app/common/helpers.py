from typing import Callable, TypeVar
from django.http import QueryDict
from rest_framework.exceptions import ParseError

T = TypeVar('T')

def get_param(
        query_params: QueryDict, 
        param: str, 
        default: T = None, 
        cast: T | Callable[[str], T] = None,
        raise_exception: bool = True
    ) -> T | str:
    """
    Get the `param` value inside a `QueryDict`.

    @query_params: QueryDict
        A QueryDict where the value will come from.
    
    @param: str
        Name or key of the param in the query string.

    @default: T, optional
        Value that will return if param does not exist. Default to True.
    
    @cast: T | (str) -> T, optional
        Function that will transform the value. If error occur, it will raise `ParseError`. 

    @raise_exception: bool, optional
        If true, it will raise exception is None is returned. Default to True.
    """
    value = query_params.get(param, default)

    if not value and raise_exception:
        raise ParseError(f"{param} does not exist")
    
    if cast:
        try:
            return cast(value)
        except:
            raise ParseError(f"Can't cast {value} ('{param}') to {cast}")
    
    return value
