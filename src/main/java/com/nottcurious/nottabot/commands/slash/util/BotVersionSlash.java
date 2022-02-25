package com.nottcurious.nottabot.commands.slash.util;

import com.nottcurious.nottabot.helpers.BotVersionHelper;
import me.s3ns3iw00.jcommands.CommandResponder;
import me.s3ns3iw00.jcommands.event.listener.CommandActionEventListener;
import me.s3ns3iw00.jcommands.event.type.CommandActionEvent;
import me.s3ns3iw00.jcommands.type.ServerCommand;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.javacord.api.DiscordApi;
import org.javacord.api.entity.message.embed.EmbedBuilder;

import java.io.IOException;

public class BotVersionSlash extends ServerCommand implements CommandActionEventListener {
    private static final Logger log = LogManager.getLogger();

    public BotVersionSlash() {
        super("botversion", "Gets the bot version");
        log.debug("Initializing BotVersionSlash");
        setOnAction(this);
    }

    @Override
    public void onAction(CommandActionEvent event) {
        CommandResponder responder = event.getResponder();

        DiscordApi api = event.getChannel().get().getApi();

        log.debug("Getting BotVersion Embed");
        EmbedBuilder embed = null;
        try {
            embed = BotVersionHelper.getBotVersionEmbed(api);
        } catch (IOException e) {
            log.fatal(e.getStackTrace());
//            e.printStackTrace();
        }

        log.info("Responding with PingEmbed");
        responder.respondNow()
                .addEmbed(embed)
                .respond();
    }
}
