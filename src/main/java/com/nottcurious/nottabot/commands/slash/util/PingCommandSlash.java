package com.nottcurious.nottabot.commands.slash.util;

import com.nottcurious.nottabot.helpers.PingHelper;
import me.s3ns3iw00.jcommands.CommandResponder;
import me.s3ns3iw00.jcommands.event.listener.CommandActionEventListener;
import me.s3ns3iw00.jcommands.event.type.CommandActionEvent;
import me.s3ns3iw00.jcommands.type.ServerCommand;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.javacord.api.entity.message.embed.EmbedBuilder;

public class PingCommandSlash extends ServerCommand implements CommandActionEventListener {
    private static final Logger log = LogManager.getLogger();

    public PingCommandSlash() {
        super("ping", "Pong!");
        log.debug("Initializing PingCommand");
        setOnAction(this);
    }

    @Override
    public void onAction(CommandActionEvent event) {
        CommandResponder responder = event.getResponder();

        log.debug("Getting Ping Embed");
        EmbedBuilder embed = PingHelper.getPingEmbed();

        log.info("Responding with PingEmbed");
        responder.respondNow()
                .addEmbed(embed)
                .respond();
    }
}
