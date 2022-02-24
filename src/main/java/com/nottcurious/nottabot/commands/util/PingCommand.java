package com.nottcurious.nottabot.commands.util;

import de.btobastian.sdcf4j.Command;
import de.btobastian.sdcf4j.CommandExecutor;
import org.javacord.api.DiscordApi;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.embed.EmbedBuilder;
import org.javacord.api.entity.server.Server;

import java.awt.*;

public class PingCommand implements CommandExecutor {
    /**
     * Executes the {@code !info} command.
     *
     * @param server  The server where the command was issued.
     * @param channel The channel where the command was issued.
     * @param message The message the command was issued in.
     */
    @Command(aliases = "..ping", async = true, description = "Pong!")
    public void handleCommand(Server server, TextChannel channel, Message message) {
        final DiscordApi api = channel.getApi();

        EmbedBuilder embed = new EmbedBuilder()
                .setColor(Color.CYAN)
                .setTitle("Pong!")
                .setThumbnail(api.getYourself().getAvatar());

        channel.sendMessage(embed).join();
    }
}
