#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2025 https://github.com/Oops19
#


from typing import Tuple

from inspect_object.pie_ctrl.user_interactions_reg import UserRegisterInteractionsInspectObjectInspect_Object1, UserRegisterInteractionsInspectObjectInspect_Object0
from sims4communitylib.enums.affordance_list_ids import CommonAffordanceListId
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.services.interactions.interaction_registration_service import CommonInteractionRegistry, CommonInteractionType, CommonScriptObjectInteractionHandler
from sims4communitylib.services.resources.common_instance_manager_modification_registry import CommonInstanceManagerModificationRegistry
from sims4communitylib.services.resources.modification_handlers.common_add_interactions_to_affordance_lists_handler import CommonAddInteractionsToAffordanceListsModificationHandler
from objects.script_object import ScriptObject


@CommonInstanceManagerModificationRegistry.register_modification_handler()
class RegisterInteractionsInspector2Inspector20a(CommonAddInteractionsToAffordanceListsModificationHandler):
    @property
    def interaction_ids(self) -> Tuple[int]:
        interactions: Tuple = (
            0x2DB7AF1A52C709E8,  # 'Inspect' - fnv('o19_Inspector2_0_PMA_Inspect_debug')
        )
        return interactions

    # noinspection PyMissingOrEmptyDocstring
    @property
    def affordance_list_ids(self) -> Tuple[int, ...]:
        result: Tuple[int, ...] = (
            CommonAffordanceListId.DEBUG_AFFORDANCES,
        )
        return result


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
class RegisterInteractionsInspectObjectInspect_Object0(CommonScriptObjectInteractionHandler):
    @property
    def interactions_to_add(self) -> Tuple[int]:
        interactions: Tuple = (
            0x2DB7AF1A52C709E8,  # 'Inspect' - fnv('o19_Inspect_Object_0_PMA_Inspect_debug')
        )
        return interactions

    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        return UserRegisterInteractionsInspectObjectInspect_Object0().should_add(self, script_object, *args, **kwargs)


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_TERRAIN_LOAD)
class RegisterInteractionsInspectObjectInspect_Object1(CommonScriptObjectInteractionHandler):
    @property
    def interactions_to_add(self) -> Tuple[int]:
        interactions: Tuple = (
            0x2DB7AF1A52C709E8,  # 'Inspect' - fnv('o19_Inspect_Object_0_PMA_Inspect_debug')
        )
        return interactions

    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        return UserRegisterInteractionsInspectObjectInspect_Object1().should_add(self, script_object, *args, **kwargs)


@CommonInstanceManagerModificationRegistry.register_modification_handler()
class RegisterPieDollDoll0_Debug(CommonAddInteractionsToAffordanceListsModificationHandler):
    @property
    def interaction_ids(self) -> Tuple[CommonInt, ...]:
        interactions: Tuple = (
            0x2DB7AF1A52C709E8,  # 'Inspect' - fnv('o19_Inspect_Object_0_PMA_Inspect_debug')
        )
        return interactions

    @property
    def affordance_list_ids(self) -> Tuple[int, ...]:
        result: Tuple[int, ...] = (
            CommonAffordanceListId.DEBUG_AFFORDANCES,
        )
        return result
