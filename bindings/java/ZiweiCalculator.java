package com.mystilink.ziwei;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

/**
 * Thin CLI wrapper. Requires mystilink-ziwei on PATH or MYSTILINK_ZIWEI_CLI.
 */
public final class ZiweiCalculator {
    private ZiweiCalculator() {}

    private static String cliPath() {
        String env = System.getenv("MYSTILINK_ZIWEI_CLI");
        if (env != null && !env.isBlank()) {
            return env;
        }
        return "mystilink-ziwei";
    }

    private static String run(List<String> command) throws Exception {
        ProcessBuilder pb = new ProcessBuilder(command);
        pb.redirectErrorStream(false);
        Process p = pb.start();
        StringBuilder stdout = new StringBuilder();
        StringBuilder stderr = new StringBuilder();
        try (BufferedReader out = new BufferedReader(
                new InputStreamReader(p.getInputStream(), StandardCharsets.UTF_8));
             BufferedReader err = new BufferedReader(
                new InputStreamReader(p.getErrorStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = out.readLine()) != null) {
                stdout.append(line).append('\n');
            }
            while ((line = err.readLine()) != null) {
                stderr.append(line).append('\n');
            }
        }
        if (!p.waitFor(120, TimeUnit.SECONDS)) {
            p.destroyForcibly();
            throw new IllegalStateException("mystilink-ziwei timed out");
        }
        if (p.exitValue() != 0) {
            String msg = stderr.length() > 0 ? stderr.toString() : stdout.toString();
            throw new IllegalStateException(msg.trim());
        }
        return stdout.toString();
    }

    public static String chart(
            String datetime,
            String timezone,
            String gender,
            String midnightZi,
            boolean siHua,
            Integer year,
            Double longitude) throws Exception {
        List<String> cmd = new ArrayList<>();
        cmd.add(cliPath());
        cmd.add("chart");
        cmd.add("--datetime");
        cmd.add(datetime);
        cmd.add("--timezone");
        cmd.add(timezone);
        cmd.add("--gender");
        cmd.add(gender);
        cmd.add("--midnight-zi");
        cmd.add(midnightZi == null || midnightZi.isBlank() ? "same-day" : midnightZi);
        if (siHua) {
            cmd.add("--si-hua");
        }
        if (year != null) {
            cmd.add("--year");
            cmd.add(Integer.toString(year));
        }
        if (longitude != null) {
            cmd.add("--longitude");
            cmd.add(Double.toString(longitude));
        }
        return run(cmd);
    }

    public static String version() throws Exception {
        List<String> cmd = new ArrayList<>();
        cmd.add(cliPath());
        cmd.add("version");
        return run(cmd);
    }
}
