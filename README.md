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

Each time a sniffer finishes digging, it makes a single roll. That roll picks either the vanilla seeds (torchflower seeds or pitcher pod) or one of the finds that's valid at that spot:

| Find | Biome | Dug block | Weight |
|---|---|---|---|
| Vanilla seeds | any | any | 20 |
| Wild armor trim | `#minecraft:is_jungle` | any | 1 |
| Coast armor trim | swamp, mangrove swamp | any | 1 |
| Dune armor trim | `#minecraft:is_badlands` | any | 1 |
| Raiser armor trim | `#minecraft:is_taiga` | any | 1 |
| Host armor trim | plains, meadow | any | 1 |
| Shaper armor trim | cherry grove | any | 1 |
| Tide armor trim | `#minecraft:is_ocean` | any | 1 |
| Wayfinder armor trim | `#c:is_snowy` | any | 1 |
| Netherite upgrade | `#minecraft:is_nether` | soul sand, soul soil | 1 |

Weights are relative to everything that's valid at the dig spot. For example, a sniffer digging grass in plains can roll the seeds (20) or host (1), so it finds a trim about 1 time in 21.

The biome and block are checked where the sniffer digs, not where it hatched. The vanilla dig cooldown is unchanged.

Snout adds soul sand and soul soil to the blocks sniffers can dig (the `minecraft:sniffer_diggable_block` tag), so a sniffer taken to the Nether can dig for netherite upgrade templates.

## Customizing with a datapack

The finds live in `data/snout/loot_table/gameplay/sniffer_digging.json`. To replace them, put a file at the same path in a datapack and run `/reload`.

The table is a normal loot table. Its first entry pulls in the vanilla sniffer table, and each find is an item entry with an optional `minecraft:location_check` condition:

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
- Keep the `minecraft:loot_table` entry, or sniffers will stop dropping seeds.

Sniffers can only dig blocks in the `minecraft:sniffer_diggable_block` tag. To make them dig a new block, add it to that tag in your datapack. Snout adds soul sand and soul soil to this tag; a datapack that sets `"replace": true` on the tag removes them.

Changes that other mods or datapacks make to the vanilla `minecraft:gameplay/sniffer_digging` table still apply, because Snout's table includes it.

## Config

`config/snout.json` is created on first launch:

```json
{
  "extraFinds": true
}
```

Set `extraFinds` to `false` to make sniffers use the vanilla loot table only. Restart the game or server after changing it.

## Building

```bash
./gradlew build
```

The jar is written to `build/libs/`. Use `./gradlew runClient` or `./gradlew runServer` to start a development instance.

## License

CC0-1.0. See [LICENSE](LICENSE).
