package maihatsuu.snout;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.storage.loot.LootTable;

/** Constants for Snout. The mod has no entrypoint: all behavior is in SnifferMixin and the data files. */
public final class Snout {
	public static final String MOD_ID = "snout";

	/** Sniffer finds, chosen per dig by biome and dug block; wraps minecraft:gameplay/sniffer_digging. */
	public static final ResourceKey<LootTable> SNIFFER_DIGGING =
			ResourceKey.create(Registries.LOOT_TABLE, id("gameplay/sniffer_digging"));

	private Snout() {
	}

	public static ResourceLocation id(String path) {
		return ResourceLocation.fromNamespaceAndPath(MOD_ID, path);
	}
}
