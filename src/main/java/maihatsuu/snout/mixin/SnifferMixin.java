package maihatsuu.snout.mixin;

import maihatsuu.snout.Snout;

import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.animal.sniffer.Sniffer;
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

	/** Roll the mod's loot table (which wraps the vanilla one) instead of the vanilla table. */
	@ModifyArg(
			method = "dropSeed",
			at = @At(
					value = "INVOKE",
					target = "Lnet/minecraft/server/ReloadableServerRegistries$Holder;getLootTable(Lnet/minecraft/resources/ResourceKey;)Lnet/minecraft/world/level/storage/loot/LootTable;"
			)
	)
	private ResourceKey<LootTable> snout$useSnoutTable(ResourceKey<LootTable> original) {
		return Snout.SNIFFER_DIGGING;
	}

	/**
	 * Move ORIGIN from the sniffer's head (in the air) to the center of the block being dug,
	 * so location_check block predicates test the dug block. Vanilla canDig() tests getHeadBlock().below().
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
		if (param == LootContextParams.ORIGIN) {
			return Vec3.atCenterOf(getHeadBlock().below());
		}
		return value;
	}
}
