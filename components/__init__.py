from .component import *
from .expression import *
from .settings import *

components: Dict[str, Component] = {}


def register_component(name: str, component: Component):
    components[name] = component


from .transformer import *

# Components
from .builtin import *
