package com.nottcurious.nottabot.logging;

import java.util.Arrays;

public class Logger {
    private final static boolean LOG_PRINT_STACK_SOURCE = false;
    private final static LogLevel minLogLevel = LogLevel.DEBUG;

    public static void debug(Object... message) {
        print(LogLevel.DEBUG, message);
    }

    public static void debugf(String msg, Object... params) {
        print(LogLevel.DEBUG, String.format(msg, params));
    }

    public static void info(Object... message) {
        print(LogLevel.INFO, message);
    }

    public static void infof(String msg, Object... params) {
        print(LogLevel.INFO, String.format(msg, params));
    }

    public static void warn(Object... message) {
        print(LogLevel.WARN, message);
    }

    public static void warnf(String msg, Object... params) {
        print(LogLevel.WARN, String.format(msg, params));
    }

    public static void fatal(Object... message) {
        print(LogLevel.FATAL, message);
    }

    public static void fatalf(String msg, Object... params) {
        print(LogLevel.FATAL, String.format(msg, params));
    }

    public static void fatal(Throwable e) {
        System.out.println(e.getMessage());
        e.printStackTrace();
    }

    public static void fatal(Throwable e, Object... message) {
        print(LogLevel.FATAL, message);
    }

    private static void print(LogLevel logLevel, Object... message) {
        if (logLevel.ordinal() >= minLogLevel.ordinal()) {
            System.out.printf("%5s: %s%n", logLevel, Arrays.toString(message));
            if (LOG_PRINT_STACK_SOURCE) {
                StackTraceElement[] stack = Thread.currentThread().getStackTrace();
                for (int i = 3; i < 6 && i < stack.length; i++) {
                    System.out.println((String.format("%40s:\t\t%s", logLevel, (stack[i].toString()))));
                }
            }
        }
    }
}
