#ifndef MYSTILINK_ZIWEI_H
#define MYSTILINK_ZIWEI_H

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Run: mystilink-ziwei chart ...
 * Returns heap-allocated JSON string (caller must free with mystilink_ziwei_free).
 * On failure returns NULL and optionally writes an error message into errbuf.
 */
char *mystilink_ziwei_chart(
    const char *datetime,
    const char *timezone,
    const char *gender,
    const char *midnight_zi, /* nullable -> same-day */
    int si_hua,
    int year,                /* 0 = omit */
    double longitude,        /* NAN = omit */
    int has_longitude,
    char *errbuf,
    unsigned errbuf_len
);

char *mystilink_ziwei_version(char *errbuf, unsigned errbuf_len);

void mystilink_ziwei_free(char *p);

#ifdef __cplusplus
}
#endif

#endif /* MYSTILINK_ZIWEI_H */
