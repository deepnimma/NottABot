package com.nottcurious.nottabot.slashcommands.util;

import me.s3ns3iw00.jcommands.CommandResponder;
import me.s3ns3iw00.jcommands.argument.ArgumentResult;
import me.s3ns3iw00.jcommands.event.listener.CommandActionEventListener;
import me.s3ns3iw00.jcommands.event.type.CommandActionEvent;
import me.s3ns3iw00.jcommands.type.ServerCommand;
import org.javacord.api.entity.message.embed.EmbedBuilder;

import java.awt.*;

public class PingCommandSlash extends ServerCommand implements CommandActionEventListener {
    public PingCommandSlash() {
        super("ping", "Pong!");
        setOnAction(this);
    }

    @Override
    public void onAction(CommandActionEvent event) {
        ArgumentResult[] args = event.getArguments();
        CommandResponder responder = event.getResponder();

        EmbedBuilder embed = new EmbedBuilder()
                .setColor(Color.CYAN)
                .setTitle("Pong!");

        responder.respondNow()
                .setContent("Pong!")
                .respond();
    }
}
