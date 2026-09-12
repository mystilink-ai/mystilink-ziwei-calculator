#ifndef MYSTILINK_ZIWEI_HPP
#define MYSTILINK_ZIWEI_HPP

#include "../c/mystilink_ziwei.h"

#include <cmath>
#include <stdexcept>
#include <string>

namespace mystilink {
namespace ziwei {

inline std::string chart(
    const std::string &datetime,
    const std::string &timezone,
    const std::string &gender,
    const std::string &midnight_zi = "same-day",
    bool si_hua = false,
    int year = 0,
    double longitude = NAN
) {
    char err[1024] = {0};
    int has_lon = std::isnan(longitude) ? 0 : 1;
    char *json = mystilink_ziwei_chart(
        datetime.c_str(),
        timezone.c_str(),
        gender.c_str(),
        midnight_zi.c_str(),
        si_hua ? 1 : 0,
        year,
        has_lon ? longitude : 0.0,
        has_lon,
        err,
        sizeof(err)
    );
    if (!json) {
        throw std::runtime_error(err[0] ? err : "mystilink_ziwei_chart failed");
    }
    std::string out(json);
    mystilink_ziwei_free(json);
    return out;
}

inline std::string version() {
    char err[1024] = {0};
    char *json = mystilink_ziwei_version(err, sizeof(err));
    if (!json) {
        throw std::runtime_error(err[0] ? err : "mystilink_ziwei_version failed");
    }
    std::string out(json);
    mystilink_ziwei_free(json);
    return out;
}

}  // namespace ziwei
}  // namespace mystilink

#endif
