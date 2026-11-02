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

Each time a sniffer finishes digging, it makes a single roll from Snout's loot table. Each find only counts if the biome and the dug block match its row below. The biome and block are checked where the sniffer digs, not where it hatched. The vanilla dig cooldown is unchanged.

Weights are relative to everything that's valid at the dig spot. If nothing is valid there, the dig drops nothing.

<!-- generated:finds -->
Besides the vanilla dig blocks, Snout lets sniffers dig clay, end stone, gravel, sand, sculk, soul sand and soul soil. Vanilla seeds (torchflower seeds or pitcher pod) only come from the vanilla dig blocks.

| Find | Count | Biome | Dug block | Weight (each) |
|---|---|---|---|---|
| Vanilla seeds | 1 | any | vanilla dig blocks² only | 20 |
| Bone Meal | 4–12 | Lush Caves | Clay, Moss Block | 10 |
| Spore Blossom, Rooted Dirt, Moss Block | 2–8 | Lush Caves | Clay, Moss Block | 10 |
| Vex Armor Trim | 1 | Dark Forest | vanilla dig blocks² | 1 |
| Wild Armor Trim | 1 | Jungle | vanilla dig blocks² | 1 |
| Globe Banner Pattern | 1 | Plains | vanilla dig blocks² | 1 |
| Sentry Armor Trim | 1 | Plains, Savanna, Desert, Snowy Plains, Taiga, Meadow, Cherry Grove, Grove, Snowy Slopes, Jagged Peaks, Frozen Peaks, Stony Peaks | vanilla dig blocks² | 1 |
| Raw Iron, Raw Gold, String, Feather, Stick, Flint, Bone | 1–4 | Overworld (all biomes) | vanilla dig blocks², sand, gravel | 1 |
| Raw Copper | 1–5 | Overworld (all biomes) | vanilla dig blocks², sand, gravel | 1 |
| Chorus Flower | 1–4 | The End (all biomes) | End Stone | 10 |
| Dragon Head | 1 | The End (all biomes) | End Stone | 3 |
| Eye Armor Trim, Spire Armor Trim | 1 | The End (all biomes) | End Stone | 1 |
| Gold Nugget, Iron Nugget | 2–8 | Beach, Snowy Beach | Sand | 5 |
| Heart of the Sea | 1 | Beach, Snowy Beach | Sand | 1 |
| Dune Armor Trim | 1 | Desert | Sand | 1 |
| Coast Armor Trim | 1 | Ocean (all variants), Beach, Snowy Beach | Sand | 1 |
| Blade Pottery Sherd, Explorer Pottery Sherd, Mourner Pottery Sherd, Plenty Pottery Sherd | 1 | Cold Ocean | Sand, Gravel | 1 |
| Archer Pottery Sherd, Miner Pottery Sherd, Prize Pottery Sherd, Skull Pottery Sherd, Arms Up Pottery Sherd, Brewer Pottery Sherd | 1 | Desert | Sand, Gravel | 1 |
| Burn Pottery Sherd, Danger Pottery Sherd, Friend Pottery Sherd, Heart Pottery Sherd, Heartbreak Pottery Sherd, Howl Pottery Sherd, Sheaf Pottery Sherd, Relic Music Disc, Wayfinder Armor Trim, Raiser Armor Trim, Shaper Armor Trim, Host Armor Trim | 1 | Trail ruins biomes¹ | Sand, Gravel | 1 |
| Angler Pottery Sherd, Shelter Pottery Sherd, Snort Pottery Sherd | 1 | Warm Ocean | Sand, Gravel | 1 |
| Candle | 4–12 | Deep Dark | Sculk | 5 |
| Echo Shard, Bottle o' Enchanting, Book | 2–8 | Deep Dark | Sculk | 5 |
| Disc Fragment | 1 | Deep Dark | Sculk | 5 |
| Otherside Music Disc, Ward Armor Trim, Silence Armor Trim | 1 | Deep Dark | Sculk | 1 |
| Nether Wart, Glowstone Dust, Gold Nugget | 4–12 | Nether Wastes, Soul Sand Valley, Crimson Forest, Warped Forest, Basalt Deltas | Soul Sand, Soul Soil | 5 |
| Crimson Nylium, Warped Nylium | 1–4 | Nether Wastes, Soul Sand Valley, Crimson Forest, Warped Forest, Basalt Deltas | Soul Sand, Soul Soil | 5 |
| Nether Quartz | 2–8 | Nether Wastes, Soul Sand Valley, Crimson Forest, Warped Forest, Basalt Deltas | Soul Sand, Soul Soil | 5 |
| Snout Banner Pattern, Netherite Upgrade, Snout Armor Trim, Rib Armor Trim | 1 | Nether Wastes, Soul Sand Valley, Crimson Forest, Warped Forest, Basalt Deltas | Soul Sand, Soul Soil | 1 |

¹ Jungle, old growth birch forest, old growth pine taiga, old growth spruce taiga, snowy taiga and taiga, where trail ruins generate.
² Dirt, grass block, podzol, coarse dirt, rooted dirt, moss block, mud and muddy mangrove roots.
<!-- /generated:finds -->

For example:

- Grass in plains: seeds (20), the eight common finds such as raw iron and string (1 each), the globe banner pattern (1) or the sentry trim (1). Seeds come up about 2 times in 3 and a rare find about 1 time in 15.
- Sand on a beach: gold or iron nuggets about half the time, and a heart of the sea about 1 time in 20.
- Sculk in the deep dark: echo shards or a disc fragment each about 1 time in 6, and the Otherside disc or a ward or silence trim about 1 time in 9.
- Soul sand in the Nether: no seeds, so every dig gives a Nether find. A netherite upgrade comes up about 1 time in 34.

## Customizing with a datapack

The finds live in `data/snout/loot_table/gameplay/sniffer_digging.json`. To replace them, put a file at the same path in a datapack and run `/reload`.

To test the table without waiting for a sniffer, stand on the block you want to test and run `/execute positioned ~ ~-0.5 ~ run loot spawn ~ ~1 ~ loot snout:gameplay/sniffer_digging`. `/loot` checks conditions at the position the command runs from, not at the spawn coordinates, so `execute positioned` moves that check into the block under you. A plain `/loot spawn ~ ~ ~ ...` checks the air at your feet and drops nothing.

It's a normal loot table. Its first entry pulls in the vanilla sniffer table, and each find is an item entry with an optional `minecraft:location_check` condition:

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
- Keep the `minecraft:loot_table` entry, or sniffers will stop dropping seeds. Its condition limits seeds to the vanilla dig blocks.
- A `biomes` or `blocks` list can't contain tags in 1.21.1. Use either a single tag or a list of IDs.

Sniffers can only dig blocks in the `minecraft:sniffer_diggable_block` tag. Snout adds the extra blocks its finds use (listed above the finds table). To make sniffers dig another block, add it to that tag in your datapack.

Changes that other mods or datapacks make to the vanilla `minecraft:gameplay/sniffer_digging` table still apply, because Snout's table includes it.

## Building

```bash
./gradlew build
```

The jar is written to `build/libs/`. Use `./gradlew runClient` or `./gradlew runServer` to start a development instance.

## License

CC0-1.0. See [LICENSE](LICENSE).
