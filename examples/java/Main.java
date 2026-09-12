// Minimal Java example. Compile with bindings/java/ZiweiCalculator.java on the classpath.
import com.mystilink.ziwei.ZiweiCalculator;

public class Main {
    public static void main(String[] args) throws Exception {
        String json = ZiweiCalculator.chart(
            "1990-05-15 14:30",
            "Asia/Shanghai",
            "male",
            "same-day",
            true,
            2026,
            121.5
        );
        System.out.println(json);
    }
}
