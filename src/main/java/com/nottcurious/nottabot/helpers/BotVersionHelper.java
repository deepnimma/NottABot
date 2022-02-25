package com.nottcurious.nottabot.helpers;

import com.nottcurious.nottabot.util.JSONGetters;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.javacord.api.DiscordApi;
import org.javacord.api.entity.message.embed.EmbedBuilder;

import java.awt.*;
import java.io.IOException;

public class BotVersionHelper {
    private static final Logger log = LogManager.getLogger();

    /**
     * Creates an embed for BotVersion normal and slash commands.
     * @param api The discordapi the bot is using
     * @return BotVersionEmbed the bot version embed
     * @throws IOException If config.json file does not exist.
     */
    public static EmbedBuilder getBotVersionEmbed(DiscordApi api) throws IOException {
        log.debug("Getting the Bot Version from config.json");
        String version = JSONGetters.getBotVersion();

        log.debug("Sending Bot Version Embed");
        return new EmbedBuilder()
                .setColor(Color.BLACK)
                .setTitle("Bot Version!")
                .setThumbnail(api.getYourself().getAvatar())
                .addField("Version", version);
    }
}
