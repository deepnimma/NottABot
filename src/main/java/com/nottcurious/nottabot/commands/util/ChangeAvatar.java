package com.nottcurious.nottabot.commands.util;

import de.btobastian.sdcf4j.Command;
import de.btobastian.sdcf4j.CommandExecutor;
import org.javacord.api.DiscordApi;
import org.javacord.api.entity.channel.TextChannel;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.server.Server;

public class ChangeAvatar implements CommandExecutor {
    /**
     * Executes the {@code !info} command.
     *
     * @param server  The server where the command was issued.
     * @param channel The channel where the command was issued.
     * @param message The message the command was issued in.
     */
    @Command(aliases = "..changepfp", async = true, description = "Changes PFP To User's Avatar")
    public void onCommand(Server server, TextChannel channel, Message message) {
        if (message.getAuthor().isBotOwner()) {
            channel.sendMessage("You are not allowed to use this command");
            return;
        }

        final DiscordApi api = channel.getApi();

        api.updateAvatar(message.getAuthor().getAvatar())
                .thenRun(() -> channel.sendMessage("Ok, I'm now using your avatar!"))
                .exceptionally(throwable -> {
                    channel.sendMessage("Something went wrong: " + throwable.getMessage());
                    return null;
                });
    }
}
