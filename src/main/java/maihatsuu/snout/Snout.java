package maihatsuu.snout;

import net.fabricmc.api.ModInitializer;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.storage.loot.LootTable;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Snout implements ModInitializer {
	public static final String MOD_ID = "snout";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	/** Overworld (and everywhere else) finds; wraps minecraft:gameplay/sniffer_digging. */
	public static final ResourceKey<LootTable> SNIFFER_DIGGING =
			ResourceKey.create(Registries.LOOT_TABLE, id("gameplay/sniffer_digging"));

	/** Finds when digging in a Nether biome. Does not include the vanilla seeds. */
	public static final ResourceKey<LootTable> NETHER_SNIFFER_DIGGING =
			ResourceKey.create(Registries.LOOT_TABLE, id("gameplay/sniffer_digging_nether"));

	/** Biomes where the Nether dig list and loot table are used instead of the vanilla ones. */
	public static final TagKey<Biome> NETHER_DIGGING_BIOMES =
			TagKey.create(Registries.BIOME, id("nether_digging"));

	/** Blocks sniffers can dig in Nether digging biomes (replaces minecraft:sniffer_diggable_block there). */
	public static final TagKey<Block> NETHER_SNIFFER_DIGGABLE =
			TagKey.create(Registries.BLOCK, id("nether_sniffer_diggable"));

	public static SnoutConfig CONFIG = new SnoutConfig();

	@Override
	public void onInitialize() {
		CONFIG = SnoutConfig.load();
	}

	/** Whether a dig at {@code dugPos} uses the Nether dig list and loot table. */
	public static boolean usesNetherDigging(Level level, BlockPos dugPos) {
		return CONFIG.extraFinds && level.getBiome(dugPos).is(NETHER_DIGGING_BIOMES);
	}

	public static ResourceLocation id(String path) {
		return ResourceLocation.fromNamespaceAndPath(MOD_ID, path);
	}
}
