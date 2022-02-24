package com.nottcurious.nottabot.commands.util;

import com.nottcurious.nottabot.util.JSONGetters;
import de.btobastian.sdcf4j.Command;
import de.btobastian.sdcf4j.CommandExecutor;
import org.javacord.api.DiscordApi;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.embed.EmbedBuilder;
import org.javacord.api.entity.server.Server;

import java.awt.*;
import java.io.IOException;

public class BotVersionCommand implements CommandExecutor {
    /**
     * Executes the {@code !info} command.
     *
     * @param server  The server where the command was issued.
     * @param channel The channel where the command was issued.
     * @param message The message the command was issued in.
     */
    @Command(aliases = "..version", async = true, description = "Gets the Bot Version!")
    public void handleCommand(Server server, TextChannel channel, Message message) throws IOException {
        String version = JSONGetters.getBotVersion();

        final DiscordApi api = channel.getApi();

        EmbedBuilder embed = new EmbedBuilder()
                .setColor(Color.BLACK)
                .setTitle("Bot Version!")
                .setThumbnail(api.getYourself().getAvatar())
                .addField("Version", version);

        channel.sendMessage(embed).join();
    }
}
