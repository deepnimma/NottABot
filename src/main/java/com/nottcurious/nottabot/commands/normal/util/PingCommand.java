package com.nottcurious.nottabot.commands.normal.util;

import com.nottcurious.nottabot.helpers.PingHelper;
import de.btobastian.sdcf4j.Command;
import de.btobastian.sdcf4j.CommandExecutor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.javacord.api.DiscordApi;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.embed.EmbedBuilder;
import org.javacord.api.entity.server.Server;

public class PingCommand implements CommandExecutor {
    private static final Logger log = LogManager.getLogger();
    /**
     * Executes the {@code !info} command.
     *
     * @param server  The server where the command was issued.
     * @param channel The channel where the command was issued.
     * @param message The message the command was issued in.
     */
    @Command(aliases = "..ping", async = true, description = "Pong!")
    public void onCommand(Server server, TextChannel channel, Message message) {
        log.info(message.getAuthor().getName() + " Used the Ping Command in " + server.getName() + " in channel " + channel.getIdAsString());
        final DiscordApi api = channel.getApi();

        EmbedBuilder embed = PingHelper.getPingEmbed();

        log.debug("Sending PingEmbed");
        channel.sendMessage(embed).join();
    }
}
