from components.logging import Logger
from components import register_component
from components.component import Component


class SlotComponent(Component):
    arguments = {}

    def run(self, args):
        slot = self.transformer.get_slot()
        if slot != None:
            self.insert_nodes_before(slot)
        else:
            Logger.logger.exit_fatal(
                f"No slot available! Are you in a §o'comp'§R component?"
            )

        self.destroy()


register_component("slot", SlotComponent)
