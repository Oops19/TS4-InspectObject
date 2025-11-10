#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2025 https://github.com/Oops19
#


import inspect
from typing import Any, Union, List

from inspect_object.modinfo import ModInfo
from interactions.context import InteractionContext
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_type_utils import CommonTypeUtils

from ts4lib.utils.singleton import Singleton

import services
import sims4.resources
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims.household import Household
from server.pick_info import PickInfo
from objects.game_object import GameObject
from objects.pools.ocean import Ocean
from objects.terrain import TerrainPoint, Terrain, OceanPoint, PoolPoint
from routing import SurfaceType, SurfaceIdentifier
from protocolbuffers import PersistenceBlobs_pb2
# noinspection PyUnresolvedReferences
from sims4.math import Vector3, Quaternion, Transform, Location

from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.utils.sims.common_sim_routing_utils import CommonSimRoutingUtils
from sims4communitylib.utils.terrain.common_terrain_location_utils import CommonTerrainLocationUtils
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'main')
log.enable()


class InspectIt(metaclass=Singleton):
    def __init__(self):
        log.info(f"Thank you for using {ModInfo.get_identity().name} ({ModInfo.get_identity().version})")
        self.log_on_test = True
        self.s4cl_location = True
        self.log_on_started = True
        self.all_properties = True
        self.mannequin = True
        self.zone = True
        self.lot = True
        self.wall = True
        self.tags = True
        self.information = True
        disable_on_load = {"s4cl_location", "all_properties", }
        self.interaction_context = None

        self.loggers = {
            "log_on_test": "Log on_test()",
            "s4cl_location": "Log S4CL location within on_test()",

            "log_on_started": "Log on_started(), log basic data, also required for the following parameters",
            "wall": "Log whether the target (TerrainObject) is a wall",
            "tags": "Log all tags of the target (GameObject)",
            "information": "Log target (GameObject) information (size, ...)",
            "mannequin": "Log mannequin (mannequin_component) information",
            "zone": "Log data about the current zone",
            "lot": "Log lot information",
            "all_properties": "Log all properties of the target object ('many' data)",
        }
        for k, v in self.loggers.items():
            if k in disable_on_load:
                setattr(self, k, False)
            log.debug(f"{getattr(self, k, None)}\t{k} ({v})")
        log.debug(f"Use 'o19.inob.toggle log_on_test' to toggle logging for 'log_on_test' etc. 'o19.inob.toggle' prints the list above to the console.")

    @staticmethod
    @CommonConsoleCommand(
        ModInfo.get_identity(), 'o19.inob.toggle', 'Print or toggle a logger',
        command_arguments=(
                CommonConsoleCommandArgument('logger', 'text', 'A logger', is_optional=True, default_value=''),
        )
    )
    def o19_cmd_toggle_loggers(output: CommonConsoleCommandOutput, logger: str = ''):
        self = InspectIt()

        if logger not in self.loggers:
            output(f"Unknown logger '{logger}'")
            logger = ''
        if logger == '':
            for k, v in self.loggers.items():
                output(f"{getattr(self, k, None)}\t{k} ({v})")
                log.debug(f"{getattr(self, k, None)}\t{k} ({v})")
            return
        setattr(self, logger, not getattr(self, logger, False))

    def on_test(self, caller, interaction_sim, interaction_target, interaction_context):
        log.debug(f"-" * 80)
        self.interaction_context = interaction_context  # persist interaction_context for on_started

        if not self.log_on_test:
            return
        log.debug(f"interaction_sim: {type(interaction_sim)} = {interaction_sim}")
        log.debug(f"interaction_target: {type(interaction_target)} = {interaction_target}")
        log.debug(f"interaction_context: {type(interaction_context)} = {interaction_context}")

        try:
            pick_info: PickInfo = getattr(interaction_context, 'pick', None)
            log.debug(f"\t.pick_info: {type(pick_info)} = {pick_info}")
            log.debug(f"\t...target: {type(getattr(pick_info, 'target', None))} = {getattr(pick_info, 'target', None)}")
            log.debug(f"\t...level: {type(getattr(pick_info, 'level', None))} = {getattr(pick_info, 'level', None)}")
            log.debug(f"\t...location: {type(getattr(pick_info, 'location', None))} = {getattr(pick_info, 'location', None)}")
            log.debug(f"\t...venue_instance = {self.get_venue_instance_from_pick_location(pick_info)}")
        except Exception as e:
            log.warn(f"Error {e}")

        self._log_4cl_location(interaction_sim, interaction_target, interaction_context)

    def on_started(self, caller, interaction_sim: Sim, interaction_target: Any):
        log.info("=" * 80)
        if not self.log_on_started:
            return

        # Basic information
        try:
            log.info(f"interaction_sim: {type(interaction_sim)} = {interaction_sim}")
            log.info(f"interaction_target: {type(interaction_target)} = {interaction_target}")
            log.debug(f"TerrainPoint / Terrain: {isinstance(interaction_target, TerrainPoint)} / {isinstance(interaction_target, Terrain)}")
            log.debug(f"OceanPoint / Ocean: {isinstance(interaction_target, OceanPoint)} / {isinstance(interaction_target, Ocean)}")
            log.debug(f"PoolPoint: {isinstance(interaction_target, PoolPoint)}")
            log.debug(f"GameObject: {isinstance(interaction_target, GameObject)}")

            if hasattr(interaction_target, 'get_household_owner_id'):
                log.info(f"\t.get_household_owner_id() = {interaction_target.get_household_owner_id()}")
            log.info(f"\t.is_sim: {type(getattr(interaction_target, 'is_sim', None))} = {getattr(interaction_target, 'is_sim', None)}")
            log.info(f"\t.StoredSimInfo: {type(getattr(interaction_target, 'StoredSimInfo', None))} = {getattr(interaction_target, 'StoredSimInfo', None)}")
            log.info(f"\t.GUID: {type(interaction_target.definition)} = {interaction_target.definition.id}")
            location = self._get_location(interaction_target)
            parent_location = None

            parent = getattr(interaction_target, 'parent', None)
            if parent:
                manager = services.object_manager()
                parent_obj = manager.get(parent.id)
                log.info(f"Parent: {type(parent)} = {parent}")
                log.info(f"Parent Object: {type(parent_obj)} = {parent_obj}")
                log.info(f"\t.GUID: {type(parent_obj.definition)} = {parent_obj.definition.id}")
                parent_location = self._get_location(parent_obj)
            else:
                log.info(f"Parent: None")
        except Exception as e:
            log.debug(f"Error {e}")

        try:
            if self.wall:
                dy = TempWall.height_above_ground(interaction_target)
                log.info(f"dy = {dy} (for TerrainPoint)")
                is_wall = TempWall.is_wall(interaction_target)
                log.info(f"is_wall = {is_wall} (for TerrainPoint)")
        except Exception as e:
            log.warn(f"Error getting height_above_ground {e}")

        try:
            if self.tags:
                if hasattr(interaction_target, 'get_tags'):
                    log.info(f"\t.get_tags: Set = {interaction_target.get_tags()}")
                    log.info(f"")
                else:
                    log.info(f"\t.get_tags: interaction_target.get_tags() is None")
        except Exception as e:
            log.debug(f"Error {e}")

        try:
            if self.information:
                # <bound method GameObject.get_edges of object_GardeningPlant_Bush_bluebell_public_garden(0x03070fc04a5c20aa)>
                log.info(f"\t.get_edges: {type(getattr(interaction_target, 'get_edges', None))} = {getattr(interaction_target, 'get_edges', None)}")

                # '00000000!d6ffc616'f080e6af.d382bf57'
                log.info(f"\t.footprint: {type(getattr(interaction_target, 'footprint', None))} = {getattr(interaction_target, 'footprint', None)}")

                # <CompoundPolygon: <Polygon{201.833450,237.519165;201.833450,236.989685;202.362930,236.989685;202.362930,237.519165 Flags='CCW'}>>
                log.info(f"\t.footprint_polygon: {type(getattr(interaction_target, 'footprint_polygon', None))} = {getattr(interaction_target, 'footprint_polygon', None)}")

                # noinspection SpellCheckingInspection
                # (Vector3Immutable(-0.383000, 0.000000, -0.383000), Vector3Immutable(0.383000, 0.000000, 0.383000))
                log.info(f"\t.get_fooptrint_polygon_bounds: {type(getattr(interaction_target, 'get_fooptrint_polygon_bounds', None))} = {getattr(interaction_target, 'get_fooptrint_polygon_bounds', None)} (typo)")
                log.info(f"\t.get_footprint_polygon_bounds(): {type(getattr(interaction_target, 'get_footprint_polygon_bounds', None))} = {getattr(interaction_target, 'get_footprint_polygon_bounds', None)} (typo fixed)")

                # <Rect((201.83, 236.99), (202.36, 237.52)>
                log.info(f"\t.get_bounding_box(): {type(getattr(interaction_target, 'get_bounding_box', None))} = {getattr(interaction_target, 'get_bounding_box', None)}")

                log.info(f"\t.is_outside() = {getattr(interaction_target, 'is_outside', None)}")  # <Rect((201.83, 236.99), (202.36, 237.52)>
                log.info(f"\t.is_inside_building = {getattr(interaction_target, 'is_inside_building', None)}")
                log.info(f"\t.flammable = {getattr(interaction_target, 'flammable', None)}")  # <Rect((201.83, 236.99), (202.36, 237.52)>
                log.info(f"\t.rig = {getattr(interaction_target, 'rig', None)}")
                log.info(f"\t.scale = {getattr(interaction_target, 'scale', None)}: {type(getattr(interaction_target, 'scale', None))}")
        except Exception as e:
            log.warn(f"Error: {e}")

        try:
            mannequin_component = getattr(interaction_target, 'mannequin_component', None)
            if self.mannequin and mannequin_component:
                log.info(f"Mannequin detected ...")

                log.info(f"mannequin_component = {mannequin_component}: {type(mannequin_component)}")
                mannequin_pose = getattr(mannequin_component, 'mannequin_pose', None)
                log.info(f"\t.mannequin_pose:: {type(mannequin_pose)} = {mannequin_pose}")
                _sim_info_data = getattr(mannequin_component, '_sim_info_data', None)
                log.info(f"\t._sim_info_data:: {type(_sim_info_data)} = {_sim_info_data}")
                if _sim_info_data:
                    sim_info = CommonSimUtils.get_sim_info(_sim_info_data)
                    if sim_info:
                        log.info(f"\t...sim_info: {type(sim_info)} = {sim_info}")

                        appearance_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
                        log.debug(f"\t...appearance_attributes: {type(appearance_attributes)} = {appearance_attributes}")
                        appearance_attributes.MergeFromString(sim_info.facial_attributes)

                        modifiers = appearance_attributes.face_modifiers
                        log.debug(f"\t...modifiers = {modifiers}: {type(modifiers)}")
                        for modifier in modifiers:
                            log.debug(f"\t...face_modifiers: {modifier.key} {modifier.amount}")

                        modifiers = appearance_attributes.body_modifiers
                        log.debug(f"\t...modifiers = {modifiers}: {type(modifiers)}")
                        for modifier in modifiers:
                            log.debug(f"\t...body_modifiers: {modifier.key} {modifier.amount}")
                    else:
                        log.warn(f"sim_info is None")
                else:
                    log.warn(f"_sim_info_data is None")
            else:
                log.info(f"Not a mannequin_component")
        except Exception as e:
            log.warn(f"Error: {e}")

        try:
            if self.lot:
                lot = services.active_lot()
                log.info(f"lot: {type(lot)} = {lot}")
                position = getattr(lot, 'position', None)
                orientation = getattr(lot, 'orientation', None)
                log.info(f"\t.position: {type(position)} = {position} (not translation !)")
                log.info(f"\t.orientation: {type(orientation)} = {orientation}")
                corners = getattr(lot, 'corners', None)
                log.info(f"\t.corners: {type(corners)} = {corners}")
                size = getattr(lot, 'size', None)
                log.info(f"\t.size: {type(size)} = {size}")
                lot_levels = getattr(lot, 'lot_levels', None)
                log.info(f"\t.lot_levels: {type(lot_levels)} = {lot_levels}")

                lot_min_x = lot_max_x = lot.center.x
                lot_min_y = lot_max_y = lot.center.y
                lot_min_z = lot_max_z = lot.center.z
                for corner in lot.corners:
                    lot_min_x = min(lot_min_x, corner.x)
                    lot_max_x = max(lot_max_x, corner.x)
                    lot_min_y = min(lot_min_y, corner.y)
                    lot_max_y = max(lot_max_y, corner.y)
                    lot_min_z = min(lot_min_z, corner.z)
                    lot_max_z = max(lot_max_z, corner.z)
                log.debug(f"\t\t{lot_min_x}/{lot_max_x} {lot_min_y}/{lot_max_y} {lot_min_z}/{lot_max_z}")
                #  ('center', Vector3(429.368225, 152.201965, 329.085388))
                # ('position', Vector3(429.368225, 152.201965, 329.085388)),
                # ('corners', (Vector3(444.368225, 152.201889, 309.085388), Vector3(414.368225, 152.202087, 309.085388), Vector3(414.368225, 152.202026, 349.085388), Vector3(444.368225, 152.201874, 349.085388))),
                # ('size', Vector3(40.000000, 15.000000, 30.000000)),
                # ('zone_id', 734946583983711787)]
                # log.debug(f"{inspect.getmembers(lot)}")

                zone = services.current_zone()
                venue = zone.venue_service.active_venue
                requires_front_door = venue.venue_requires_front_door
                household_id = zone.lot.owner_household_id
                household: Household = services.household_manager().get(household_id)
                # state_setting = household.autonomy_settings.get_setting(AutonomyState, AutonomySettingsGroup.DEFAULT)
                # for sim_info in household.sim_info_gen():
                log.debug(f"current_zone.zone_id = {zone.id}, current_zone.venue = {venue}, requires_front_door={requires_front_door}, owner_household_id={household_id}")
                log.debug(f"Household:")
                for sim_id in household.get_sims_at_home():
                    sim_info: SimInfo = CommonSimUtils.get_sim_info(sim_id)
                    log.debug(f"\t...sim_info: {sim_info} ({sim_id})")
        except Exception as e:
            log.debug(f"Error {e}")

        # TODO add more lot/venu info f(TS4Library)
        # TODO clean this mess up
        venue_instance = self.get_venue_instance_from_pick_location(interaction_target)  # : VenueService  ?
        log.debug(f"venue_instance: {venue_instance}: {type(venue_instance)} ")

        try:
            log.debug(f"interaction_target: {inspect.getmembers(interaction_target)}")
            zone = services.current_zone()
            log.debug(f"Zone id/neighborhood_id/open_street_id/lot: {zone.id}/{zone.neighborhood_id}/{zone.open_street_id}/{zone.lot}")
            if self.zone:
                log.debug(f"{inspect.getmembers(zone)}")

            zone_manager = services.get_zone_manager()
            # ....
        except Exception as e:
            log.debug(f"Error {e}")

        self._log_properties(interaction_target)

    def get_venue_instance_from_pick_location(self, pick: PickInfo):
        try:
            if pick is None:
                return
            lot_id = pick.lot_id
            if lot_id is None:
                return
            else:

                persistence_service = services.get_persistence_service()
                lot_owner_info = persistence_service.get_lot_proto_buff(lot_id)
                if lot_owner_info is not None:
                    venue_tuning_id = lot_owner_info.venue_key
                    venue_instance = services.get_instance_manager(sims4.resources.Types.VENUE).get(venue_tuning_id)
                    log.debug(f"{venue_instance}")
                    return venue_instance
        except Exception as e:
            log.debug(f"get_venue_instance_from_pick_location error {e}")
            return None

    def _log_properties(self, interaction_target: Any):
        log.debug(f"\t...has_any_tag = {getattr(interaction_target, 'has_any_tag', None)}")
        log.debug(f"\t...num_properties = {len(dir(interaction_target))}")
        if not self.all_properties:
            return
        try:
            _i_error: List[str] = []
            _i_skip: List[str] = []
            _i_none: List[str] = []
            _i_true: List[str] = []
            _i_false: List[str] = []
            _i_zero: List[str] = []
            _i_methods: List[str] = []
            _i_callables: List[str] = []
            for _i in dir(interaction_target):
                i = "?"
                # noinspection PyBroadException
                try:
                    i = f"{_i}"
                    v = getattr(interaction_target, i)
                except Exception:
                    _i_error.append(i)
                    continue

                if i.startswith("__"):
                    _i_skip.append(i)
                elif inspect.ismethod(v) or inspect.isfunction(v):
                    _i_methods.append(i)
                elif callable(v):
                    _i_callables.append(i)
                elif v is None:
                    _i_none.append(i)
                elif isinstance(v, bool):
                    (_i_true if v else _i_false).append(i)
                elif isinstance(v, int) and v == 0:
                    _i_zero.append(i)
                else:
                    log.debug(f"\t...{i}: {type(v)} = {v}")
            # log summary for similar values
            if _i_error:
                log.debug(f"\t...Errors = {_i_error}")
            if _i_skip:
                log.debug(f"\t...Skipped = {_i_skip}")
            if _i_none:
                log.debug(f"\t...None = {_i_none}")
            if _i_true:
                log.debug(f"\t...True = {_i_true}")
            if _i_false:
                log.debug(f"\t...False = {_i_false}")
            if _i_zero:
                log.debug(f"\t...int=0 = {_i_zero}")
            if _i_methods:
                log.debug(f"\t...Methods = {_i_methods}")
            if _i_callables:
                log.debug(f"\t...Callables = {_i_callables}")
        except Exception as e:
            log.warn(f"Error {e}")

    def _get_location(self, interaction_target: Any) -> Location:
        r"""
        Print and return the location of the 'interaction_target', whatever it is.
        Prints also whether the translation (position) is on or off the active lot.
        :param interaction_target:
        :return:
        """
        location = getattr(interaction_target, 'location', None)
        if location:
            log.info(f"\t.location: {type(location)} = {location}")
        else:
            location = getattr(interaction_target, '_location', None)
            if location:
                log.info(f"\t._location: {type(location)} = {location} (with '_')")
        if location:
            transform = getattr(location, 'transform', None)
            translation = getattr(transform, 'translation', None)
            orientation = getattr(transform, 'orientation', None)
            log.info(f"\t...translation: {type(translation)} = {translation}")
            log.info(f"\t...orientation: {type(orientation)} = {orientation}")

            # do not use services.active_lot()
            is_position_on_lot = services.current_zone().lot.is_position_on_lot(translation)
            log.info(f"\t...is_position_on_lot: = {is_position_on_lot}")
        return location

    def _log_4cl_location(self, interaction_sim, interaction_target, interaction_context):
        r"""
        Log location and routing information as S4CL handles it internally.
        There seems to be no difference between can_route_to_terrain)= and can_route_to_pick_target_of_interaction_context()
        :param interaction_sim:
        :param interaction_target:
        :param interaction_context:
        :return:
        """
        if not self.s4cl_location:
            return
        # As S4CL figures out location and surface

        try:
            sim_info = CommonSimUtils.get_sim_info(interaction_sim)
            log.debug(f"can_route_to_terrain = {CommonSimRoutingUtils.can_route_to_terrain(sim_info, interaction_target)}")
            log.debug(f"can_route_to_pick_target_of_interaction_context = {CommonSimRoutingUtils.can_route_to_pick_target_of_interaction_context(sim_info, interaction_context)}")
        except Exception as e:
            log.warn(f"Error {e}")

        try:
            position = CommonTerrainLocationUtils.get_position(interaction_target)
            routing_surface = CommonTerrainLocationUtils.get_routing_surface(interaction_target)
            log.debug(f"position: {type(position)} = {position} f(interaction_target)")
            log.debug(f"routing_surface: {type(routing_surface)} = {routing_surface} f(interaction_target)")
        except Exception as e:
            log.warn(f"error {e}")

        pick_info = 'pick_info'
        pick_target = 'pick_info'
        location = 'location'
        _routing_surface = 'routing_surface'
        try:
            pick_info = getattr(interaction_context, 'pick', None)
            location = getattr(pick_info, 'location', None)
            _routing_surface = getattr(pick_info, 'routing_surface', None)
            position = CommonVector3.from_vector3(location)
            routing_surface = CommonSurfaceIdentifier.from_surface_identifier(_routing_surface)
            log.debug(f"position: {type(position)} = {position} f(interaction_context)")
            log.debug(f"routing_surface: {type(routing_surface)} = {routing_surface} f(interaction_context)")
            pick_target = getattr(pick_info, 'target', None)
            if pick_target and CommonTypeUtils.is_water(pick_target):
                sim_info = CommonSimUtils.get_sim_info(interaction_sim)
                log.debug(f"can_swim_at_position:  {CommonSimRoutingUtils.can_swim_at_position(sim_info, position, routing_surface)}")
        except Exception as e:
            log.debug(f"pick_info:  {type(pick_info)} = {pick_info}")
            log.debug(f"pick_target:  {type(pick_target)} = {pick_target}")
            log.debug(f"location:  {type(location)} = {location}")
            log.warn(f"Error {e}")


class TempWall:
    @classmethod
    def is_wall(cls, terrain_point: TerrainPoint, tolerance: int = 0.1, double_check_tolerance: int = 3.5, sim_info=None, level: int = None, interaction_context=None) -> Union[bool, None]:
        """
        For TerrainPoints outside the current lot 'None' is returned
        For non-TerrainPoint objects random results are returned.
        :param terrain_point:
        :param tolerance:
        :param double_check_tolerance: Check whether the TerrainPoint is routable for small height offsets. Specify sim_info and/or interaction_context to use this option.
        :param interaction_context: Needed to gather the right level when clicked on a wall. Otherwise, 'level' is used.
        :param sim_info:
        :return:
        """
        if cls.is_position_on_lot(terrain_point) is None:
            return None

        if abs(cls.height_above_ground(terrain_point, level, interaction_context)) > tolerance:
            # it seems to be a wall
            if abs(cls.height_above_ground(terrain_point)) < double_check_tolerance:
                # check also routing
                if cls.can_route_to(terrain_point, sim_info, interaction_context):
                    return False
            return True
        return False

    @classmethod
    def can_route_to(cls, terrain_point: TerrainPoint, sim_info=None, interaction_context=None):
        if sim_info is None:
            sim_info = CommonSimUtils.get_active_sim_info()
        if CommonSimRoutingUtils.can_route_to_terrain(sim_info, terrain_point):
            return True
        if interaction_context and CommonSimRoutingUtils.can_route_to_pick_target_of_interaction_context(sim_info, interaction_context):
            return True
        return False

    @classmethod
    def is_position_on_lot(cls, terrain_point: TerrainPoint) -> bool:
        return services.current_zone().lot.is_position_on_lot(cls._get_translation(terrain_point))

    @classmethod
    def height_above_ground(cls, terrain_point: TerrainPoint, level: int = None, interaction_context: InteractionContext = None) -> float:
        r"""
        :param terrain_point: The terrain point to check. Without further parameters level=0 is used as the 'ground' reference.
        :param level: The level to use a 'ground' reference, if missing 'interaction_context' is used.
        :param interaction_context: 2nd options to retrieve the level to use a 'ground' reference. If also this option is missing level=0 is used.
        :return: The difference to the 'ground level'' on the current lot. Might be positive or negative
        Returns 1000.0 if not on lot.
        Returns 1100.0 if it fails
        --
        For lots the value may be negative or positive when clicking on a wall.
        For Sulani the beach area has TerrainPoint values from 0 - 0.5 for places where sims can walk in water.
        Pond returns a TerrainPoint: The value is usually negative
        Pool returns a PoolPoint: The value is often -0.125
        Sea returns an OceanPoint: The value will be positive as the surface point is above the ground.
        """
        if cls.is_position_on_lot(terrain_point) is None:
            return 1000.0
        if level is None:
            pick_info: PickInfo = getattr(interaction_context, 'pick', None)
            level = getattr(pick_info, 'level', 0)

        dy = 1100.0
        try:
            translation = cls._get_translation(terrain_point)
            zone_id = services.current_zone_id()
            surface = int(SurfaceType.SURFACETYPE_WORLD)
            _routing_surface = SurfaceIdentifier(zone_id, level, surface)
            y = services.terrain_service.terrain_object().get_routing_surface_height_at(translation.x, translation.z, _routing_surface)
            dy = translation.y - y
        except Exception as e:
            log.warn(f"Could not get y position for {TerrainPoint}: {type(TerrainPoint)} ({e})")
        return dy

    @classmethod
    def _get_translation(cls, terrain_point: TerrainPoint):  # Vector3
        # translation = translation.location.transform.translation
        # translation = translation._location.transform.translation  # for objects or sims?
        return getattr(getattr(getattr(terrain_point, 'location', getattr(terrain_point, '_location', None)), 'transform', None), 'translation', None)
