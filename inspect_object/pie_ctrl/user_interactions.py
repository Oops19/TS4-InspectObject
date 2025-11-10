#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2025 https://github.com/Oops19
#


from typing import Any

from inspect_object.inspect_it import InspectIt

from sims.sim import Sim
from event_testing.results import TestResult
from interactions.context import InteractionContext

from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult


class UserInteractionsInspectObject:
    @classmethod
    def on_test(cls, caller, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        InspectIt().on_test(caller, interaction_sim, interaction_target, interaction_context)
        return TestResult.TRUE

    def on_started(self, caller, interaction_sim: Sim, interaction_target: Any) -> bool:
        InspectIt().on_started(caller, interaction_sim, interaction_target)
        return CommonExecutionResult.TRUE
