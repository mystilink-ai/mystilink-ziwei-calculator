# Build hints (examples)

## C
```bash
cc -o run_chart main.c ../../bindings/c/mystilink_ziwei.c
./run_chart
```

## C++
```bash
c++ -o run_chart main.cpp ../../bindings/c/mystilink_ziwei.c
./run_chart
```

## C#
```bash
# Add ../../bindings/csharp/ZiweiCalculator.cs to your project, then run Program.cs
```

## Java
```bash
javac -d out ../../bindings/java/ZiweiCalculator.java Main.java
java -cp out Main
```

Requires `mystilink-ziwei` on PATH after `pip install -e .`.
