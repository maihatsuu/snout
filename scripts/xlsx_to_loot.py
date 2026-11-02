#!/usr/bin/env python3
"""Generate Snout's loot table, dig tag and README finds table from the spreadsheet.

Usage (from the repo root):
    python3 scripts/xlsx_to_loot.py ["../Sniffer Loot Tables.xlsx"]

Spreadsheet: first sheet, header row, then one row per find:
    Item | Count | Biome | Diggable Block | Weight
- Item: display name ("Echo Shard", "Wild Armor Trim"); see ITEM_ALIASES for names that differ from the ID.
- Count: "1" or a range like "2-8".
- Biome / Diggable Block: comma-separated display names, or an entry in BIOME_ALIASES.
- Every row becomes one weighted entry in a single table, with a location_check on its biome and block.

Writes (relative to the repo root):
    src/main/resources/data/snout/loot_table/gameplay/sniffer_digging.json
    src/main/resources/data/minecraft/tags/block/sniffer_diggable_block.json (blocks the rows use, beyond vanilla)
    README.md (between the <!-- generated:finds --> markers)

IDs are checked against the Minecraft jar in the Fabric Loom cache (run ./gradlew build once first).
Requires openpyxl (pip install --user openpyxl) and a JDK (javap) for the ID check.
"""
import glob
import json
import os
import re
import subprocess
import sys
import zipfile

import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "src/main/resources/data")
README = os.path.join(ROOT, "README.md")
DEFAULT_XLSX = os.path.join(ROOT, "..", "Sniffer Loot Tables.xlsx")
MC_VERSION = "1.21.1"

ITEM_ALIASES = {
    "Snout Banner Pattern": "piglin_banner_pattern",
    "Disc Fragment": "disc_fragment_5",
    "Otherside Music Disc": "music_disc_otherside",
    "Relic Music Disc": "music_disc_relic",
    "Netherite Upgrade": "netherite_upgrade_smithing_template",
    "Bottle o' Enchanting": "experience_bottle",
    "Nether Quartz": "quartz",
}
# Spreadsheet names for vanilla biome tags. Used as-is when it's the only biome in a cell; inside a list it's
# expanded to its members (read from the game jar), because 1.21.1 biome/block lists can't contain tags.
BIOME_ALIASES = {
    "Ocean (all variants)": "is_ocean",
    "The End (all biomes)": "is_end",
    "Overworld (all biomes)": "is_overworld",
}
VANILLA_DIG = ["dirt", "grass_block", "podzol", "coarse_dirt", "rooted_dirt", "moss_block", "mud",
               "muddy_mangrove_roots"]
SEEDS_WEIGHT = 20

# README display shortcuts for long lists that appear on many rows.
README_SHORT = {
    "Jungle, Old Growth Birch Forest, Old Growth Pine Taiga, Old Growth Spruce Taiga, Snowy Taiga, Taiga":
        ("Trail ruins biomes¹", "¹ Jungle, old growth birch forest, old growth pine taiga, old growth spruce taiga, "
                                "snowy taiga and taiga, where trail ruins generate."),
    "Coarse Dirt, Dirt, Grass Block, Moss Block, Mud, Muddy Mangrove Roots, Rooted Dirt, Podzol":
        ("vanilla dig blocks²", None),
    "Coarse Dirt, Dirt, Grass Block, Moss Block, Mud, Muddy Mangrove Roots, Rooted Dirt, Podzol, Sand, Gravel":
        ("vanilla dig blocks², sand, gravel", None),
}
VANILLA_FOOTNOTE = ("² Dirt, grass block, podzol, coarse dirt, rooted dirt, moss block, mud and "
                    "muddy mangrove roots.")


def known_ids():
    """Biome, item and block IDs from the Loom-cached Minecraft jar, or None if it can't be found."""
    pattern = os.path.expanduser(
        f"~/.gradle/caches/fabric-loom/minecraftMaven/net/minecraft/minecraft-common/{MC_VERSION}-*/*.jar")
    jars = [j for j in glob.glob(pattern) if not j.endswith("-sources.jar")]
    if not jars:
        print(f"warning: no Minecraft {MC_VERSION} jar in the Loom cache; IDs not checked", file=sys.stderr)
        return None
    jar = jars[0]
    with zipfile.ZipFile(jar) as z:
        biomes = {os.path.basename(n)[:-5] for n in z.namelist()
                  if n.startswith("data/minecraft/worldgen/biome/") and n.endswith(".json")}
        tag_dir = "data/minecraft/tags/worldgen/biome/"
        biome_tags = {n[len(tag_dir):-5]: json.loads(z.read(n))["values"] for n in z.namelist()
                      if n.startswith(tag_dir) and n.endswith(".json")}

    def strings(cls):
        out = subprocess.run(["javap", "-c", "-constants", "-cp", jar, cls],
                             capture_output=True, text=True, check=True).stdout
        return set(re.findall(r"String ([a-z0-9_]+)$", out, re.M))

    things = strings("net.minecraft.world.item.Items") | strings("net.minecraft.world.level.block.Blocks")
    return biomes, things, biome_tags


def snake(s):
    return re.sub(r"[^a-z0-9]+", "_", s.strip().lower()).strip("_")


def split(cell):
    return [x.strip() for x in re.split(r"[,.]", str(cell)) if x.strip()]


class Converter:
    def __init__(self, ids):
        self.ids = ids
        self.errors = []

    def check(self, kind, name, i):
        if self.ids is None:
            return
        biomes, things, _ = self.ids
        if i not in (biomes if kind == "biome" else things):
            self.errors.append(f"unknown {kind} '{name}' (looked for minecraft:{i})")

    def item(self, name):
        if name in ITEM_ALIASES:
            i = ITEM_ALIASES[name]
        elif name.endswith("Armor Trim"):
            i = snake(name[:-len("Armor Trim")]) + "_armor_trim_smithing_template"
        else:
            i = snake(name)
        self.check("item", name, i)
        return "minecraft:" + i

    def tag_members(self, tag):
        """Plain biome IDs in a vanilla biome tag, following nested tags."""
        if self.ids is None:
            self.errors.append(f"can't expand #minecraft:{tag} without the Minecraft jar")
            return []
        tags = self.ids[2]
        if tag not in tags:
            self.errors.append(f"unknown biome tag #minecraft:{tag}")
            return []
        out = []
        for v in tags[tag]:
            v = v.removeprefix("minecraft:")
            out += self.tag_members(v[len("#minecraft:"):]) if v.startswith("#") else [v]
        return out

    def biomes(self, cell):
        """Returns (json value, plain biome IDs)."""
        names = [x.strip() for x in str(cell).split(",") if x.strip()]
        if len(names) == 1 and names[0] in BIOME_ALIASES:
            tag = BIOME_ALIASES[names[0]]
            return "#minecraft:" + tag, self.tag_members(tag)
        ids = []
        for n in names:
            if n in BIOME_ALIASES:
                ids += [i for i in self.tag_members(BIOME_ALIASES[n]) if i not in ids]
            else:
                ids.append(snake(n))
                self.check("biome", n, snake(n))
        full = ["minecraft:" + i for i in ids]
        return (full[0] if len(full) == 1 else full), ids

    def blocks(self, cell):
        ids = []
        for n in split(cell):
            ids.append(snake(n))
            self.check("block", n, snake(n))
        full = ["minecraft:" + i for i in ids]
        return (full[0] if len(full) == 1 else full), ids


def count_range(cell):
    lo, _, hi = str(cell).strip().partition("-")
    lo = int(float(lo))
    hi = int(float(hi)) if hi else lo
    return lo, hi


def table(entries, seq):
    return {"type": "minecraft:gift",
            "pools": [{"rolls": 1.0, "bonus_rolls": 0.0, "entries": entries}],
            "random_sequence": seq}


def dump(rel, obj):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(json.dumps(obj, indent=2) + "\n")


def readme_table(rows):
    groups, notes = {}, []
    for r in rows:
        b, bnote = README_SHORT.get(r["biome"], (r["biome"], None))
        k, knote = README_SHORT.get(r["block"], (r["block"], None))
        for note in (bnote, knote):
            if note and note not in notes:
                notes.append(note)
        key = (r["count"].replace("-", "–"), b, k, r["weight"])
        groups.setdefault(key, []).append(r["name"])
    lines = ["| Find | Count | Biome | Dug block | Weight (each) |", "|---|---|---|---|---|"]
    lines.append(f"| Vanilla seeds | 1 | any | vanilla dig blocks² only | {SEEDS_WEIGHT} |")
    for (c, b, k, w), names in groups.items():
        lines.append(f"| {', '.join(names)} | {c} | {b} | {k} | {w} |")
    footer = notes + [VANILLA_FOOTNOTE]
    return "\n".join(lines) + ("\n\n" + "\n".join(footer) if footer else "")


def replace_generated(text, name, body):
    start, end = f"<!-- generated:{name} -->", f"<!-- /generated:{name} -->"
    pattern = re.compile(re.escape(start) + ".*?" + re.escape(end), re.S)
    if not pattern.search(text):
        print(f"warning: README has no {start} markers; skipped", file=sys.stderr)
        return text
    return pattern.sub(lambda _: f"{start}\n{body}\n{end}", text)


def nice(ids):
    names = [i.replace("_", " ") for i in ids]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def main():
    xlsx = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_XLSX
    conv = Converter(known_ids())
    ws = openpyxl.load_workbook(xlsx).worksheets[0]

    entries, dig, rows = [], [], []
    for n, r in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if not r or not r[0]:
            continue
        name, count, biome, block, weight = (list(r) + [None] * 5)[:5]
        name = str(name).strip()
        try:
            lo, hi = count_range(count if count is not None else 1)
            weight = int(float(weight))
        except (TypeError, ValueError):
            conv.errors.append(f"row {n} ({name}): bad count '{count}' or weight '{weight}'")
            continue
        e = {"type": "minecraft:item", "name": conv.item(name), "weight": weight}
        if (lo, hi) != (1, 1):
            e["functions"] = [{"function": "minecraft:set_count",
                               "count": lo if lo == hi else {"type": "minecraft:uniform", "min": lo, "max": hi}}]
        pred = {}
        if biome:
            pred["biomes"], _ = conv.biomes(biome)
        block_ids = []
        if block:
            blocks_json, block_ids = conv.blocks(block)
            pred["block"] = {"blocks": blocks_json}
        if pred:
            e["conditions"] = [{"condition": "minecraft:location_check", "predicate": pred}]

        entries.append(e)
        dig += [b for b in block_ids if b not in dig]
        rows.append({"name": name, "count": f"{lo}-{hi}" if lo != hi else str(lo), "biome": str(biome or "any"),
                     "block": str(block or "any"), "weight": weight})

    if conv.errors:
        print("Spreadsheet errors (nothing written):", *conv.errors, sep="\n  ", file=sys.stderr)
        sys.exit(1)

    seeds = {"type": "minecraft:loot_table", "value": "minecraft:gameplay/sniffer_digging", "weight": SEEDS_WEIGHT,
             "conditions": [{"condition": "minecraft:location_check",
                             "predicate": {"block": {"blocks": ["minecraft:" + b for b in VANILLA_DIG]}}}]}
    dump("snout/loot_table/gameplay/sniffer_digging.json", table([seeds] + entries, "snout:gameplay/sniffer_digging"))
    extra = sorted(b for b in dig if b not in VANILLA_DIG)
    dump("minecraft/tags/block/sniffer_diggable_block.json",
         {"replace": False, "values": ["minecraft:" + b for b in extra]})

    with open(README) as f:
        text = f.read()
    intro = (f"Besides the vanilla dig blocks, Snout lets sniffers dig {nice(extra)}. " if extra else "") + \
        "Vanilla seeds (torchflower seeds or pitcher pod) only come from the vanilla dig blocks."
    text = replace_generated(text, "finds", intro + "\n\n" + readme_table(rows))
    with open(README, "w") as f:
        f.write(text)

    print(f"{len(entries)} finds")
    print(f"dig additions: {', '.join(extra) or 'none'}")
    print("Check the hand-written odds examples in README.md if weights changed.")


if __name__ == "__main__":
    main()
