# Snout

A Fabric mod for Minecraft 1.21.1 that lets sniffers dig up more than seeds. Depending on the biome they're in and the block they dig, sniffers can now turn up armor trim smithing templates.

All finds come from a loot table, so datapacks can change, remove or add to them without touching any code.

## Requirements

- Minecraft 1.21.1
- Fabric Loader 0.20.1 or newer
- Fabric API
- Java 21

Snout is **server-side only**. Install it on the server (or in singleplayer); players can join with an unmodded client.

## Finds

Each time a sniffer finishes digging, it makes a single roll from one of two loot tables, chosen by the biome where it digs. The biome and block are checked where the sniffer digs, not where it hatched. The vanilla dig cooldown is unchanged.

Weights are relative to everything that's valid at the dig spot. If nothing is valid there, the dig drops nothing.

### Overworld and the End

<!-- generated:overworld -->
Besides the vanilla dig blocks, Snout lets sniffers dig clay, end stone, sand, sculk, suspicious gravel and suspicious sand. Vanilla seeds (torchflower seeds or pitcher pod) only come from the vanilla dig blocks.

| Find | Count | Biome | Dug block | Weight (each) |
|---|---|---|---|---|
| Vanilla seeds | 1 | any | vanilla dig blocks² only | 20 |
| Globe Banner Pattern | 1 | Plains | vanilla dig blocks² | 1 |
| Burn Pottery Sherd, Danger Pottery Sherd, Friend Pottery Sherd, Heart Pottery Sherd, Heartbreak Pottery Sherd, Howl Pottery Sherd, Sheaf Pottery Sherd, Relic Music Disc, Wayfinder Armor Trim, Raiser Armor Trim, Shaper Armor Trim, Host Armor Trim | 1 | Trail ruins biomes¹ | Suspicious Sand, Suspicious Gravel | 1 |
| Archer Pottery Sherd, Miner Pottery Sherd, Prize Pottery Sherd, Skull Pottery Sherd, Arms Up Pottery Sherd, Brewer Pottery Sherd | 1 | Desert | Suspicious Sand, Suspicious Gravel | 1 |
| Angler Pottery Sherd, Shelter Pottery Sherd, Snort Pottery Sherd | 1 | Warm Ocean | Suspicious Sand, Suspicious Gravel | 1 |
| Blade Pottery Sherd, Explorer Pottery Sherd, Mourner Pottery Sherd, Plenty Pottery Sherd | 1 | Cold Ocean | Suspicious Sand, Suspicious Gravel | 1 |
| Disc Fragment, Otherside Music Disc, Ward Armor Trim, Silence Armor Trim | 1 | Deep Dark | Sculk | 1 |
| Echo Shard | 2–8 | Deep Dark | Sculk | 10 |
| Heart of the Sea | 1 | Beach, Snowy Beach | Sand | 1 |
| Spore Blossom | 2–8 | Lush Caves | Clay, Moss Block | 10 |
| Sentry Armor Trim | 1 | Plains, Savanna, Desert, Snowy Plains, Taiga, Meadow, Cherry Grove, Grove, Snowy Slopes, Jagged Peaks, Frozen Peaks, Stony Peaks | vanilla dig blocks² | 1 |
| Vex Armor Trim | 1 | Dark Forest | vanilla dig blocks² | 1 |
| Wild Armor Trim | 1 | Jungle | vanilla dig blocks² | 1 |
| Coast Armor Trim | 1 | Ocean (all variants), Beach, Snowy Beach | Sand | 1 |
| Dune Armor Trim | 1 | Desert | Sand | 1 |
| Eye Armor Trim, Spire Armor Trim | 1 | The End (all biomes) | End Stone | 1 |

¹ Jungle, old growth birch forest, old growth pine taiga, old growth spruce taiga, snowy taiga and taiga, where trail ruins generate.
² Dirt, grass block, podzol, coarse dirt, rooted dirt, moss block, mud and muddy mangrove roots.
<!-- /generated:overworld -->

For example, a sniffer digging grass in plains can roll the seeds (20), the globe banner pattern (1) or the sentry trim (1), so it finds something other than seeds about 1 time in 11. Digging sculk in the deep dark gives echo shards 10 times in 14.

### Nether

<!-- generated:nether -->
In Nether biomes, sniffers can only dig soul sand and soul soil, and roll a separate table with no seeds:

| Find | Count | Biome | Dug block | Weight (each) |
|---|---|---|---|---|
| Snout Banner Pattern, Netherite Upgrade, Snout Armor Trim, Rib Armor Trim | 1 | Nether Wastes, Soul Sand Valley, Crimson Forest, Warped Forest | Soul Sand, Soul Soil | 1 |
<!-- /generated:nether -->

Every dig on soul sand or soul soil in these biomes gives one of the four finds.

## Customizing with a datapack

The finds live in two loot tables:

- `data/snout/loot_table/gameplay/sniffer_digging.json` for everywhere outside the Nether
- `data/snout/loot_table/gameplay/sniffer_digging_nether.json` for Nether biomes

To replace either, put a file at the same path in a datapack and run `/reload`.

These are normal loot tables. The overworld table's first entry pulls in the vanilla sniffer table, and each find is an item entry with an optional `minecraft:location_check` condition:

```json
{
  "type": "minecraft:gift",
  "pools": [
    {
      "rolls": 1,
      "entries": [
        {
          "type": "minecraft:loot_table",
          "value": "minecraft:gameplay/sniffer_digging",
          "weight": 20
        },
        {
          "type": "minecraft:item",
          "name": "minecraft:coast_armor_trim_smithing_template",
          "weight": 1,
          "conditions": [
            {
              "condition": "minecraft:location_check",
              "predicate": {
                "biomes": ["minecraft:swamp", "minecraft:mangrove_swamp"],
                "block": { "blocks": ["minecraft:mud", "minecraft:muddy_mangrove_roots"] }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

- `biomes` takes a biome ID, a biome tag (`#minecraft:is_forest`) or a list.
- `block.blocks` takes a block ID, a block tag (`#minecraft:dirt`) or a list. You can add `block.state` to match block state properties.
- Leave out the condition to make an item droppable anywhere.
- In the overworld table, keep the `minecraft:loot_table` entry, or sniffers will stop dropping seeds. Its condition limits seeds to the vanilla dig blocks.
- A `biomes` or `blocks` list can't contain tags in 1.21.1. Use either a single tag or a list of IDs.

Which blocks sniffers can dig, and where the Nether rules apply, are also tags:

| Tag | Default | Controls |
|---|---|---|
| `snout:nether_digging` (biome) | `#minecraft:is_nether` | Biomes that use the Nether dig list and loot table |
| `snout:nether_sniffer_diggable` (block) | soul sand, soul soil | Blocks sniffers can dig in those biomes |
| `minecraft:sniffer_diggable_block` (block) | vanilla dig blocks, plus sand, suspicious sand, suspicious gravel, clay, sculk, end stone | Blocks sniffers can dig everywhere else |

Add to a tag in your datapack to extend it, or set `"replace": true` to replace it.

Changes that other mods or datapacks make to the vanilla `minecraft:gameplay/sniffer_digging` table still apply, because Snout's table includes it.

## Config

`config/snout.json` is created on first launch:

```json
{
  "extraFinds": true
}
```

Set `extraFinds` to `false` to make sniffers fully vanilla: they use the vanilla loot table and dig list everywhere, and can't dig in the Nether. Restart the game or server after changing it.

## Building

```bash
./gradlew build
```

The jar is written to `build/libs/`. Use `./gradlew runClient` or `./gradlew runServer` to start a development instance.

## License

CC0-1.0. See [LICENSE](LICENSE).
