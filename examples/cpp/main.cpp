// Minimal C++ example — compile with ../../bindings/c/mystilink_ziwei.c
#include <iostream>
#include "../../bindings/cpp/mystilink_ziwei.hpp"

int main() {
    try {
        std::string json = mystilink::ziwei::chart(
            "1990-05-15 14:30",
            "Asia/Shanghai",
            "male",
            "same-day",
            true,
            2026,
            121.5
        );
        std::cout << json;
    } catch (const std::exception &ex) {
        std::cerr << ex.what() << std::endl;
        return 1;
    }
    return 0;
}
