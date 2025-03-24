from typing import Dict, Any, List, Optional, Union, Set, Callable, TypeVar
import os
from pathlib import Path
T = TypeVar('T')
def validate_path(path: Union[str, Path], must_exist: bool = False, 
                 create_dir: bool = False) -> Path:
    path_obj = Path(path) if isinstance(path, str) else path
    if create_dir and not path_obj.exists():
        path_obj.mkdir(parents=True, exist_ok=True)
    if must_exist and not path_obj.exists():
        raise FileNotFoundError(f"Path does not exist: {path_obj}")
    return path_obj
def validate_env_var(name: str, default: Optional[str] = None) -> str:
    value = os.environ.get(name, default)
    if value is None:
        raise ValueError(f"Required environment variable not set: {name}")
    return value
def validate_dict_key(d: Dict[str, Any], key: str, 
                     default: Optional[T] = None) -> T:
    if not isinstance(d, dict):
        return default
    return d.get(key, default)
def validate_executable(cmd: str) -> bool:
    return any(os.access(os.path.join(p, cmd), os.X_OK)
              for p in os.environ["PATH"].split(os.pathsep)
              if os.path.exists(os.path.join(p, cmd)))
def ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, (str, bytes)):
        return [value]
    try:
        return list(value)
    except:
        return [value]
def safe_call(func: Callable[..., T], *args, default: T = None, 
             **kwargs) -> T:
    try:
        return func(*args, **kwargs)
    except Exception:
        return default