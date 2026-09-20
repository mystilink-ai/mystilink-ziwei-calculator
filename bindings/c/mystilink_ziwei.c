#include "mystilink_ziwei.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef MYSTILINK_ZIWEI_CLI_DEFAULT
#define MYSTILINK_ZIWEI_CLI_DEFAULT "ziwei"
#endif

static const char *cli_path(void) {
    const char *env = getenv("MYSTILINK_ZIWEI_CLI");
    if (env && env[0]) {
        return env;
    }
    return MYSTILINK_ZIWEI_CLI_DEFAULT;
}

static void set_err(char *errbuf, unsigned errbuf_len, const char *msg) {
    if (!errbuf || errbuf_len == 0) {
        return;
    }
    snprintf(errbuf, errbuf_len, "%s", msg ? msg : "unknown error");
}

static char *read_all(FILE *fp) {
    size_t cap = 4096;
    size_t len = 0;
    char *buf = (char *)malloc(cap);
    if (!buf) {
        return NULL;
    }
    for (;;) {
        if (len + 1024 > cap) {
            cap *= 2;
            char *n = (char *)realloc(buf, cap);
            if (!n) {
                free(buf);
                return NULL;
            }
            buf = n;
        }
        size_t nread = fread(buf + len, 1, 1024, fp);
        len += nread;
        if (nread < 1024) {
            break;
        }
    }
    buf[len] = '\0';
    return buf;
}

static char *run_cmd(const char *cmd, char *errbuf, unsigned errbuf_len) {
    FILE *fp = popen(cmd, "r");
    if (!fp) {
        set_err(errbuf, errbuf_len, "popen failed");
        return NULL;
    }
    char *out = read_all(fp);
    int status = pclose(fp);
    if (!out) {
        set_err(errbuf, errbuf_len, "out of memory");
        return NULL;
    }
    if (status != 0) {
        set_err(errbuf, errbuf_len, out[0] ? out : "cli failed");
        free(out);
        return NULL;
    }
    return out;
}

char *mystilink_ziwei_chart(
    const char *datetime,
    const char *timezone,
    const char *gender,
    const char *midnight_zi,
    int si_hua,
    int year,
    double longitude,
    int has_longitude,
    char *errbuf,
    unsigned errbuf_len
) {
    if (!datetime || !timezone || !gender) {
        set_err(errbuf, errbuf_len, "datetime, timezone, gender required");
        return NULL;
    }
    const char *mz = midnight_zi && midnight_zi[0] ? midnight_zi : "same-day";
    char cmd[2048];
    int n = snprintf(
        cmd,
        sizeof(cmd),
        "%s chart --datetime \"%s\" --timezone \"%s\" --gender \"%s\" --midnight-zi \"%s\"",
        cli_path(),
        datetime,
        timezone,
        gender,
        mz
    );
    if (n < 0 || (size_t)n >= sizeof(cmd)) {
        set_err(errbuf, errbuf_len, "command too long");
        return NULL;
    }
    if (si_hua) {
        strncat(cmd, " --si-hua", sizeof(cmd) - strlen(cmd) - 1);
    }
    if (year > 0) {
        char tmp[64];
        snprintf(tmp, sizeof(tmp), " --year %d", year);
        strncat(cmd, tmp, sizeof(cmd) - strlen(cmd) - 1);
    }
    if (has_longitude) {
        char tmp[64];
        snprintf(tmp, sizeof(tmp), " --longitude %.6f", longitude);
        strncat(cmd, tmp, sizeof(cmd) - strlen(cmd) - 1);
    }
    return run_cmd(cmd, errbuf, errbuf_len);
}

char *mystilink_ziwei_version(char *errbuf, unsigned errbuf_len) {
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "%s version", cli_path());
    return run_cmd(cmd, errbuf, errbuf_len);
}

void mystilink_ziwei_free(char *p) {
    free(p);
}
