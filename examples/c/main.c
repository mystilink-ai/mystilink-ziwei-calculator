/* Minimal C example — link with ../../bindings/c/mystilink_ziwei.c */
#include <stdio.h>
#include "../../bindings/c/mystilink_ziwei.h"

int main(void) {
    char err[1024] = {0};
    char *json = mystilink_ziwei_chart(
        "1990-05-15 14:30",
        "Asia/Shanghai",
        "male",
        "same-day",
        1,
        2026,
        121.5,
        1,
        err,
        sizeof(err)
    );
    if (!json) {
        fprintf(stderr, "error: %s\n", err);
        return 1;
    }
    fputs(json, stdout);
    mystilink_ziwei_free(json);
    return 0;
}
