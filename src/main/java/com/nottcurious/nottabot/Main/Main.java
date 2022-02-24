package com.nottcurious.nottabot.main;

//import com.nottcurious.nottabot.logging.Logger;

import com.nottcurious.nottabot.commands.util.BotVersionCommand;
import com.nottcurious.nottabot.commands.util.PingCommand;
import com.nottcurious.nottabot.util.JSONGetters;
import de.btobastian.sdcf4j.CommandHandler;
import de.btobastian.sdcf4j.handler.JavacordHandler;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.javacord.api.DiscordApi;
import org.javacord.api.DiscordApiBuilder;
import org.javacord.api.util.logging.ExceptionLogger;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
    private static final Logger log = LogManager.getLogger();

    public static void main(String[] args) throws IOException {
        setupLogging();

        log.info("Getting Secrets");
        String token = JSONGetters.getBotToken();

        log.info("Creating DiscordAPI Object");
        DiscordApi api = new DiscordApiBuilder().setToken(token).login().join();
        log.info("Bot Online and Logged In");

        log.info("Creating CommandHandler");
        CommandHandler handler = new JavacordHandler(api);

        log.info("Adding Commands");

        log.debug("Adding Util Commands");
        handler.registerCommand(new PingCommand());
        handler.registerCommand(new BotVersionCommand());
        log.debug("Finished Adding Util Commands");

        log.info("Finished Adding Commands");
    }

    private static void setupLogging() throws IOException {
        System.setProperty("java.util.logging.manager", org.apache.logging.log4j.jul.LogManager.class.getName());

        String log4jConfigurationFileProperty = System.getProperty("log4j.configurationFile");
        if (log4jConfigurationFileProperty != null) {
            Path log4jConfigurationFile = Paths.get(log4jConfigurationFileProperty);
            if (!Files.exists(log4jConfigurationFile)) {
                try (InputStream fallbackLog4j2ConfigStream = Main.class.getResourceAsStream("/log4j2.xml")) {
                    assert fallbackLog4j2ConfigStream != null;
                    Files.copy(fallbackLog4j2ConfigStream, log4jConfigurationFile);
                }
            }
        }

        Thread.setDefaultUncaughtExceptionHandler(ExceptionLogger.getUncaughtExceptionHandler());
    }
}
