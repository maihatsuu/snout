package maihatsuu.snout;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonParseException;

import net.fabricmc.loader.api.FabricLoader;

import java.io.IOException;
import java.io.Reader;
import java.io.Writer;
import java.nio.file.Files;
import java.nio.file.Path;

/** Plain JSON config at config/snout.json. */
public class SnoutConfig {
	private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();

	/** When false, sniffers roll the vanilla loot table unchanged. */
	public boolean extraFinds = true;

	private static Path path() {
		return FabricLoader.getInstance().getConfigDir().resolve(Snout.MOD_ID + ".json");
	}

	public static SnoutConfig load() {
		Path path = path();
		SnoutConfig config = null;

		if (Files.exists(path)) {
			try (Reader reader = Files.newBufferedReader(path)) {
				config = GSON.fromJson(reader, SnoutConfig.class);
			} catch (IOException | JsonParseException e) {
				Snout.LOGGER.warn("Could not read {}, using defaults", path, e);
				return new SnoutConfig();
			}
		}

		if (config == null) {
			config = new SnoutConfig();
		}
		// Rewrite so new options appear in existing files.
		config.save();
		return config;
	}

	public void save() {
		Path path = path();
		try {
			Files.createDirectories(path.getParent());
			try (Writer writer = Files.newBufferedWriter(path)) {
				GSON.toJson(this, writer);
			}
		} catch (IOException e) {
			Snout.LOGGER.warn("Could not write {}", path, e);
		}
	}
}
