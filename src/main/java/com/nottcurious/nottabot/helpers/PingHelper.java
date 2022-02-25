package com.nottcurious.nottabot.helpers;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.javacord.api.entity.message.embed.EmbedBuilder;

import java.awt.*;

public class PingHelper {
    private static final Logger log = LogManager.getLogger();

    /**
     * Returns the Embed required for the Ping normal and slash commands.
     * @return the Ping Embed.
     */
    public static EmbedBuilder getPingEmbed() {
        log.debug("Returning Pong! Embed");
        return new EmbedBuilder()
                .setColor(Color.CYAN)
                .setTitle("Pong!");
    }
}
