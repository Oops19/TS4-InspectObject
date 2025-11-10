# 🔎 TS4 Inspect Object
A mod for script mod developers and curious players interested in inspecting object properties in The Sims 4.

This mod logs detailed information about game objects to its log file.

Logging occurs during `on_test()` and `on_started()` whenever objects are clicked, which may noticeably slow down the game.
This mod is not intended for regular gameplay and should be disabled in production or casual play sessions.

## 🛠️ Usage
Shift-click on a Sim (limited support), terrain, game object, or pool to log information about the selected target.

## ⚙️ Options
The mod supports several filters that can be toggled via the cheat console.
Each filter controls what kind of data is logged:

* `log_on_test`: Logs on_test()
* `s4cl_location`: Logs S4CL location data within on_test().
* `log_on_started`: Logs on_started() and basic object data. Required for the filters below.
* `wall`: Logs whether the target (TerrainObject) is a wall.
* `tags`: Logs all tags associated with the target (for GameObject).
* `information`: Logs general information about the target (GameObject), such as size.
* `mannequin`: Logs mannequin data from the mannequin_component.
* `zone`: Logs data about the current zone.
* `lot`: Logs information about the current lot.
* `all_properties`: Logs all properties of the target object ('many' data).

### 🕵️️ Cheat Commands
To toggle a filter, use the following cheat format:
```code
o19.inob.toggle <filter_name>
```
For example:
```code
o19.inob.toggle log_on_test
```
Calling the cheat without a parameter will log the current state of all filters.

# 📄 Sample Output
For example, inspecting a chair parented to a table may produce output like:
```text
interaction_sim: <class 'sims4.tuning.instances.object_sim'> = Dina#Caliente
interaction_target: <class 'sims4.tuning.instances.object_chair_dining'> = object_chair_dining:0x059b153fff120236
 TerrainPoint / Terrain: False / False
 OceanPoint / Ocean: False / False
 PoolPoint: False
 GameObject: True
	.get_household_owner_id() = 74051199549841765
	.is_sim: <class 'bool'> = False
	.StoredSimInfo: <class 'NoneType'> = None
	.GUID: <class 'objects.definition.Definition'> = 260356
	.location: <class 'sims4.math.Location'> = Location(Transform(Vector3(0.701569, 0.000000, 0.000031), Quaternion(0.000000, 0.707107, 0.000000, -0.707106)), None, joint_name_or_hash=None, parent=object_tableDining_1x1:0x059b153fff1101d2[2], slot_hash=204485742)
	...translation: <class 'Vector3Immutable'> = Vector3Immutable(0.701569, 0.000000, 0.000031)
	...orientation: <class 'QuaternionImmutable'> = QuaternionImmutable(0.000000, 0.707107, 0.000000, -0.707106)
	...is_position_on_lot: = False
Parent: <class 'sims4.tuning.instances.Part(object_tableDining_1x1)'> = object_tableDining_1x1:0x059b153fff1101d2[2]
Parent Object: <class 'sims4.tuning.instances.object_tableDining_1x1'> = object_tableDining_1x1:0x059b153fff1101d2
	.GUID: <class 'objects.definition.Definition'> = 260197
	.location: <class 'sims4.math.Location'> = Location(Transform(Vector3(181.082993, 150.876389, 171.644028), Quaternion(0.000000, -0.385488, 0.000000, 0.922713)), {107152C745C1FD7,0,World}, joint_name_or_hash=None, parent=None, slot_hash=0)
	...translation: <class 'Vector3Immutable'> = Vector3Immutable(181.082993, 150.876389, 171.644028)
	...orientation: <class 'QuaternionImmutable'> = QuaternionImmutable(0.000000, -0.385488, 0.000000, 0.922713)
	...is_position_on_lot: = True

	.get_edges: <class 'method'> = <bound method GameObject.get_edges of object_chair_dining(0x059b153fff120236)>
	.footprint: <class '_resourceman.Key'> = '00000000!4efae3f6'aeed7f62.d382bf57'
	.footprint_polygon: <class 'sims4.geometry.CompoundPolygon'> = <CompoundPolygon: <Polygon{181.547226,171.729095;182.064194,172.252365;181.672516,172.639313;181.155563,172.116028;181.094391,171.655609 Flags='CCW'}>>
	.get_fooptrint_polygon_bounds: <class 'method'> = <bound method HasFootprintComponent.get_fooptrint_polygon_bounds of object_chair_dining(0x059b153fff120236)> (typo)
	.get_footprint_polygon_bounds(): <class 'NoneType'> = None (typo fixed)
	.get_bounding_box(): <class 'method'> = <bound method HasFootprintComponent.get_bounding_box of object_chair_dining(0x059b153fff120236)>
	.is_outside() = False
	.is_inside_building = False
	.flammable = True
	.rig = '00000000!1194cab6'7150d15f.8eaf13de'
	.scale = 1: <class 'int'>

lot: <class 'world.lot.Lot'> = <world.lot.Lot object at 0x00007FF41EBEDD88>
	.position: <class 'Vector3'> = Vector3(176.083069, 149.874878, 171.613647) (not translation !)
	.orientation: <class 'Quaternion'> = Quaternion(0.000000, 0.704955, 0.000000, 0.709252)
	.corners: <class 'tuple'> = (Vector3(165.992126, 149.873352, 186.552612), Vector3(185.991760, 149.873413, 186.674118), Vector3(186.174026, 149.876404, 156.674667), Vector3(166.174393, 149.890121, 156.553162))
	.size: <class 'Vector3'> = Vector3(30.000000, 23.000000, 20.000000)

```

## 🧪 Notes
This mod is primarily useful for debugging or exploring object internals. Some features are already available in other mods:

* Object states and running interactions for Sims are covered by S4CL.
* Venue names are available via TS4Lib.
* `mannequin_component` was added to support debugging and to enable mannequin compatibility with the [Copy Outfits](https://github.com/Oops19/TS4-CopyOutfits) mods a while ago.
* Additional data may be added in future updates.

---

# 📝 Addendum

## 🔄 Game compatibility
This mod has been tested with `The Sims 4` 1.119.109, S4CL 3.15, TS4Lib 0.3.42.
It is expected to remain compatible with future releases of TS4, S4CL, and TS4Lib.

## 📦 Dependencies
Download the ZIP file - not the source code.
Required components:
* [This Mod](../../releases/latest)
* [TS4-Library](https://github.com/Oops19/TS4-Library/releases/latest)
* [S4CL](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases/latest)
* [The Sims 4](https://www.ea.com/games/the-sims/the-sims-4)

If not already installed, download and install TS4 and the listed mods. All are available for free.

## 📥 Installation
* Locate the localized `The Sims 4` folder (it contains the `Mods` folder).
* Extract the ZIP file directly into this folder.

This will create:
* `Mods/_o19_/$mod_name.ts4script`
* `Mods/_o19_/$mod_name.package`
* `mod_data/$mod_name/*`
* `mod_documentation/$mod_name/*` (optional)
* `mod_sources/$mod_name/*` (optional)

Additional notes:
* CAS and Build/Buy UGC without scripts will create `Mods/o19/$mod_name.package`.
* A log file `mod_logs/$mod_name.txt` will be created once data is logged.
* You may safely delete `mod_documentation/` and `mod_sources/` folders if not needed.

### 📂 Manual Installation
If you prefer not to extract directly into `The Sims 4`, you can extract to a temporary location and copy files manually:
* Copy `mod_data/` contents to `The Sims 4/mod_data/` (usually required).
* `mod_documentation/` is for reference only — not required.
* `mod_sources/` is not needed to run the mod.
* `.ts4script` files can be placed in a folder inside `Mods/`, but storing them in `_o19_` is recommended for clarity.
* `.package` files can be placed in a anywhere inside `Mods/`.

## 🛠️ Troubleshooting
If installed correctly, no troubleshooting should be necessary.
For manual installs, verify the following:
* Does your localized `The Sims 4` folder exist? (e.g. localized to Die Sims 4, Les Sims 4, Los Sims 4, The Sims 4, ...)
  * Does it contain a `Mods/` folder?
    * Does Mods/_o19_/ contain:
      * `ts4lib.ts4script` and `ts4lib.package`?
      * `{mod_name}.ts4script` and/or `{mod_name}.package`
* Does `mod_data/` contain `{mod_name}/` with files?
* Does `mod_logs/` contain:
  * `Sims4CommunityLib_*_Messages.txt`?
  * `TS4-Library_*_Messages.txt`?
  * `{mod_name}_*_Messages.txt`?
* Are there any `last_exception.txt` or `last_exception*.txt` files in `The Sims 4`?


* When installed properly this is not necessary at all.
For manual installations check these things and make sure each question can be answered with 'yes'.
* Does 'The Sims 4' (localized to Die Sims 4, Les Sims 4, Los Sims 4, The Sims 4, ...) exist?
  * Does `The Sims 4` contain the folder `Mods`?
    * Does `Mods` contain the folder `_o19_`? 
      * Does `_19_` contain `ts4lib.ts4script` and `ts4lib.package` files?
      * Does `_19_` contain `{mod_name}.ts4script` and/or `{mod_name}.package` files?
  * Does `The Sims 4` contain the folder `mod_data`?
    * Does `mod_data` contain the folder `{mod_name}`?
      * Does `{mod_name}` contain files or folders?
  * Does `The Sims 4` contain the `mod_logs` ?
    * Does `mod_logs` contain the file `Sims4CommunityLib_*_Messages.txt`?
    * Does `mod_logs` contain the file `TS4-Library_*_Messages.txt`?
      * Is this the most recent version or can it be updated?
    * Does `mod_logs` contain the file `{mod_name}_*_Messages.txt`?
      * Is this the most recent version or can it be updated?
  * Doesn't `The Sims 4` contain the file(s) `last_exception.txt`  and/or `last_exception*.txt` ?
* Share the `The Sims 4/mod_logs/Sims4CommunityLib_*_Messages.txt` and `The Sims 4/mod_logs/{mod_name}_*_Messages.txt`  file.

If issues persist, share:
`mod_logs/Sims4CommunityLib_*_Messages.txt`
`mod_logs/{mod_name}_*_Messages.txt`

## 🕵️ Usage Tracking / Privacy
This mod does not send any data to external servers.
The code is open source, unobfuscated, and fully reviewable.

Note: Some log entries (especially warnings or errors) may include your local username if file paths are involved.
Share such logs with care.

## 🔗 External Links
[Sources](https://github.com/Oops19/)
[Support](https://discord.gg/d8X9aQ3jbm)
[Donations](https://www.patreon.com/o19)

## ⚖️ Copyright and License
* © 2020-2025 [Oops19](https://github.com/Oops19)
* `.package` files: [Electronic Arts TOS for UGC](https://tos.ea.com/legalapp/WEBTERMS/US/en/PC/)  
* All other content (unless otherwise noted): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 

You may use and adapt this mod and its code — even without owning The Sims 4.
Have fun extending or integrating it into your own mods!

Oops19 / o19 is not affiliated with or endorsed by Electronic Arts or its licensors.
Game content and materials © Electronic Arts Inc. and its licensors.
All trademarks are the property of their respective owners.

## 🧾 Terms of Service
* Do not place this mod behind a paywall.
* Avoid creating mods that break with every TS4 update.
* For simple tuning mods, consider using:
  * [Patch-XML](https://github.com/Oops19/TS4-PatchXML) 
  * [LiveXML](https://github.com/Oops19/TS4-LiveXML).
* To verify custom tuning structures, use:
  * [VanillaLogs](https://github.com/Oops19/TS4-VanillaLogs).

## 🗑️ Removing the Mod
Installing this mod creates files in several directories. To fully remove it, delete:
* `The Sims 4/Mods/_o19_/$mod_name.*`
* `The Sims 4/mod_data/_o19_/$mod_name/`
* `The Sims 4/mod_documentation/_o19_/$mod_name/`
* `The Sims 4/mod_sources/_o19_/$mod_name/`

To remove all of my mods, delete the following folders:
* `The Sims 4/Mods/_o19_/`
* `The Sims 4/mod_data/_o19_/`
* `The Sims 4/mod_documentation/_o19_/`
* `The Sims 4/mod_sources/_o19_/`
