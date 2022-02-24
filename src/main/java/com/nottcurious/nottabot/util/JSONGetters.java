package com.nottcurious.nottabot.util;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class JSONGetters {
    private static final Logger log = LogManager.getLogger();

    /**
     * Returns the bot token
     *
     * @return token The bot token
     * @throws IOException In case file does not exist
     */
    public static String getBotToken() throws IOException {
        log.debug("Getting JSON Data");
        String data = new String(Files.readAllBytes(Paths.get("./src/main/resources/token.json")));

        log.debug("Creating JSON Object for SecretData");
        JSONObject jsonObject = new JSONArray(data).getJSONObject(0);

        log.info("Returning Token");
        return jsonObject.get("token").toString();
    }

    /**
     * Returns the Hypixel API Key Stored
     *
     * @return String Hypixel API Key
     * @throws IOException In case file does not exist
     */
    public static String getAPIKey() throws IOException {
        log.debug("Getting JSON Data");
        String data = new String(Files.readAllBytes(Paths.get("./src/main/resources/token.json")));

        log.debug("Creating JSON Object for SecretData");
        JSONObject jsonObject = new JSONArray(data).getJSONObject(0);

        log.info("Returning APIKey");
        return jsonObject.get("hypixel_api_key").toString();
    }

    /**
     * Returns Bot Version
     *
     * @return String Bot Version
     * @throws IOException In case file does not exist
     */
    public static String getBotVersion() throws IOException {
        log.debug("Getting JSON Data");
        String data = new String(Files.readAllBytes(Paths.get("./src/main/resources/config.json")));

        log.debug("Created JSON Object for Config");
        JSONObject jsonObject = new JSONArray(data).getJSONObject(0);

        log.info("Returning Bot Version");
        return jsonObject.get("bot_version").toString();
    }
}
