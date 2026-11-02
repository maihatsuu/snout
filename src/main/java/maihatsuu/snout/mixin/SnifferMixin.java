package maihatsuu.snout.mixin;

import com.llamalad7.mixinextras.sugar.Local;

import maihatsuu.snout.Snout;

import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceKey;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.animal.sniffer.Sniffer;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.storage.loot.LootTable;
import net.minecraft.world.level.storage.loot.parameters.LootContextParam;
import net.minecraft.world.level.storage.loot.parameters.LootContextParams;
import net.minecraft.world.phys.Vec3;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyArg;

@Mixin(Sniffer.class)
public abstract class SnifferMixin {
	@Shadow
	private BlockPos getHeadBlock() {
		throw new AssertionError();
	}

	/** The block the sniffer digs. Vanilla canDig() tests getHeadBlock().below(). */
	private BlockPos snout$dugPos() {
		return getHeadBlock().below();
	}

	/** In Nether digging biomes, test the Nether dig list instead of minecraft:sniffer_diggable_block. */
	@ModifyArg(
			method = "canDig(Lnet/minecraft/core/BlockPos;)Z",
			at = @At(
					value = "INVOKE",
					target = "Lnet/minecraft/world/level/block/state/BlockState;is(Lnet/minecraft/tags/TagKey;)Z"
			)
	)
	private TagKey<Block> snout$netherDiggable(TagKey<Block> original, @Local(argsOnly = true) BlockPos pos) {
		Sniffer self = (Sniffer) (Object) this;
		return Snout.usesNetherDigging(self.level(), pos) ? Snout.NETHER_SNIFFER_DIGGABLE : original;
	}

	/** Roll the mod's loot table (overworld or Nether) instead of the vanilla table. */
	@ModifyArg(
			method = "dropSeed",
			at = @At(
					value = "INVOKE",
					target = "Lnet/minecraft/server/ReloadableServerRegistries$Holder;getLootTable(Lnet/minecraft/resources/ResourceKey;)Lnet/minecraft/world/level/storage/loot/LootTable;"
			)
	)
	private ResourceKey<LootTable> snout$useSnoutTable(ResourceKey<LootTable> original) {
		if (!Snout.CONFIG.extraFinds) {
			return original;
		}
		Sniffer self = (Sniffer) (Object) this;
		return Snout.usesNetherDigging(self.level(), snout$dugPos()) ? Snout.NETHER_SNIFFER_DIGGING : Snout.SNIFFER_DIGGING;
	}

	/**
	 * Move ORIGIN from the sniffer's head (in the air) to the center of the block being dug,
	 * so location_check block predicates test the dug block.
	 */
	@ModifyArg(
			method = "dropSeed",
			at = @At(
					value = "INVOKE",
					target = "Lnet/minecraft/world/level/storage/loot/LootParams$Builder;withParameter(Lnet/minecraft/world/level/storage/loot/parameters/LootContextParam;Ljava/lang/Object;)Lnet/minecraft/world/level/storage/loot/LootParams$Builder;"
			),
			index = 1
	)
	private Object snout$moveOriginToDugBlock(LootContextParam<?> param, Object value) {
		if (param == LootContextParams.ORIGIN && Snout.CONFIG.extraFinds) {
			return Vec3.atCenterOf(snout$dugPos());
		}
		return value;
	}
}
