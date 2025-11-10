#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2025 https://github.com/Oops19
#


from typing import Any

from event_testing.results import TestResult
from inspect_object.pie_ctrl.user_interactions import UserInteractionsInspectObject
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction


# Do not modify the class name. It is referenced in the Package.
#class InteractionsInspector2(CommonTerrainInteraction):
class InteractionsInspectObject(CommonImmediateSuperInteraction):

    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        return UserInteractionsInspectObject().on_test(cls, interaction_sim, interaction_target, interaction_context)

    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        return UserInteractionsInspectObject().on_started(self, interaction_sim, interaction_target)
