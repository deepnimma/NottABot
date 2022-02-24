package com.nottcurious.nottabot.main;

import com.nottcurious.nottabot.util.SecretsGetters;
import org.javacord.api.util.logging.ExceptionLogger;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) throws IOException {
        setupLogging();

        String token = SecretsGetters.getBotToken();
        String api_key = SecretsGetters.getAPIKey();
        System.out.println(token + api_key);
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
