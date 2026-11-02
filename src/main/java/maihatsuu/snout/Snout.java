package maihatsuu.snout;

import net.fabricmc.api.ModInitializer;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.storage.loot.LootTable;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Snout implements ModInitializer {
	public static final String MOD_ID = "snout";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	/** Sniffer finds, chosen per dig by biome and dug block; wraps minecraft:gameplay/sniffer_digging. */
	public static final ResourceKey<LootTable> SNIFFER_DIGGING =
			ResourceKey.create(Registries.LOOT_TABLE, id("gameplay/sniffer_digging"));

	public static SnoutConfig CONFIG = new SnoutConfig();

	@Override
	public void onInitialize() {
		CONFIG = SnoutConfig.load();
	}

	public static ResourceLocation id(String path) {
		return ResourceLocation.fromNamespaceAndPath(MOD_ID, path);
	}
}
