---
description: 用于定义如何写单元测试的规则（JUnit4 + PowerMock）
---

# 单元测试规则 - JUnit4 + PowerMock

务必使用 powermock 和 junit4

## 测试文件命名规范
- 测试类名必须以 `Test` 结尾
- 测试类应该与被测试类在相同的包结构下，位于 `src/test/java` 目录
- 例如：`CalculateFirstBudgetBo.java` 对应的测试类应该是 `CalculateFirstBudgetBoTest.java`
- 应首先查看同名的测试包下是否有对应的测试类，如果有，则优先学习测试类里的单元测试写法。
- 请直接在对应的类进行单元测试的增加。例如`CalculateFirstBudgetBoTest.java`！！！！

## 测试类结构

### 1. 基本注解配置
必须是以下两种形式
```java
@RunWith(SafePowerMockRunner.class)  // 使用SafePowerMockRunner 如果项目里有这个类的话
@PrepareForTest({ClassName.class})  // 需要mock静态类的时候使用
public class ClassNameTest {
    // 测试代码
}
```

```java
@RunWith(PowerMockRunner.class)  // 使用PowerMockRunner 
@PrepareForTest({ClassName.class})  // 需要mock静态类的时候使用
public class ClassNameTest {
    // 测试代码
}
```

### 2. 依赖注入和Mock配置
```java
@InjectMocks
private ClassName className;  // 被测试的类

@Mock
private DependencyService dependencyService;  // 依赖的服务

@Mock
private AnotherService anotherService;
```

### 3. 测试方法命名规范
- 测试方法名应该清晰描述测试场景
- 使用 `test` 前缀或描述性名称
- 例如：`testGetSegmentInfo()`, `testConvertStringMoney_ValidInput()`

## 测试方法编写规范

### 1. 基本测试方法结构
```java
@Test
public void testMethodName() {
    // Given - 准备测试数据
    // When - 执行被测试方法
    // Then - 验证结果
}
```

### 2. Mock配置示例
```java

// PowerMock配置
PowerMockito.when(budget.getPredictAmount()).thenReturn(10);
PowerMockito.when(budget.getBudgetItems()).thenReturn(items);
```

### 3. 断言使用
```java
// JUnit断言
Assert.assertEquals(expected, actual);
Assert.assertNotNull(result);

// AssertJ断言（推荐）
assertThat(result).isEqualByComparingTo(new BigDecimal("1234.56"));
assertThat(result).isNull();
```

## PowerMock使用规范

### 1. 静态方法Mock
```java
@PrepareForTest({StaticClass.class})
public class TestClass {
    @Test
    public void testStaticMethod() {
        PowerMockito.mockStatic(StaticClass.class);
        PowerMockito.when(StaticClass.staticMethod()).thenReturn("mocked");
    }
}
```

### 2. 私有方法测试
```java
@Test
public void testPrivateMethod() throws Exception {
    Class clazz = ClassName.class;
    Method method = clazz.getDeclaredMethod("privateMethodName", String.class);
    method.setAccessible(true);
    Object result = method.invoke(className, "parameter");
}
```

### 3. 字段注入测试
```java
@Test
public void testFieldInjection() throws Exception {
    Field field = ClassName.class.getDeclaredField("fieldName");
    field.setAccessible(true);
    field.set(className, mockValue);
}
```

## 测试数据准备

### 1. 实体对象创建
```java
TourBudgetEntity budget = new TourBudgetEntity();
budget.setChannel("");
budget.setProductId(1006595974L);
budget.setDepartureCity("2");
budget.setDepartureDate(new Timestamp(1706198400000L));
budget.setPredictAmount(1);
```

### 2. Mock对象创建
```java
ProductInfoType productInfo = new ProductInfoType();
BasicInfoType basicInfoType = new BasicInfoType();
basicInfoType.setMinPersonQuantity(2);
productInfo.setBasicInfo(basicInfoType);
```

## 测试覆盖场景

### 1. 正常流程测试
- 测试正常输入下的预期输出
- 验证业务逻辑的正确性

### 2. 边界条件测试
- 测试空值、null值处理
- 测试边界数值
- 测试异常情况

### 3. 异常处理测试
```java
@Test(expected = IllegalArgumentException.class)
public void testInvalidInput() {
    // 测试异常情况
}
```

## 最佳实践
1. 每个测试方法只测试一个功能点
2. 测试方法名要清晰表达测试意图
3. 使用合适的断言方法
4. 合理使用Mock减少外部依赖
5. 保持测试代码的可读性和可维护性
6. 测试覆盖率要达到合理水平

## ⚡ 写单元测试高效 SOP（避免常见坑）

### 开局策略（前 5 分钟）
1. **不要提前大规模代码探索**
   - ❌ 先把所有源文件、枚举、entity 都读一遍再写
   - ✅ 直接看现有同类测试，学框架写法
2. **快速定位缺口**
   - 打开被测试类源码 + 现有测试文件并排看
   - 标记未覆盖的分支（null 检查、异常处理、各个方法等）
   - 这一步不超过 3 分钟

### 编写阶段（主要工作）
3. **边写边改，不做前置 mock 完美化**
   - 直接写测试 → 编译 → 看错误 → 改
   - 常见错误：
     - `throws Exception` → `throws Throwable`（涉及 ProceedingJoinPoint.proceed）
     - Mockito matcher 不配对：`when(obj.method(arg))` 需要 `when(obj.method(eq(arg)))`
     - 不能 mock final 类（如 `java.lang.reflect.Method`）→ 用真实对象或反射调用
     - **写 mock 前先看 repo/dao 方法是否 `throws SQLException`**：`when(repo.method(...))` 调用处会触发受检异常检查，有则测试方法加 `throws Exception`，否则编译报错
4. **分组测试，便于维护**
   - 按被测试方法分组，用注释标记：`// ─── sendTourBaseChange tests ───`
   - 每个方法群 2-3 个测试（正常 + 边界）

### 验证阶段
5. **一次验证，不逐个运行**
   - `mvn test -Dtest=Class1Test,Class2Test` 同时验证
   - 看 `Tests run: XX, Failures: 0, Errors: 0` 一行确认全部通过
6. **任何时候验证改动，只跑本次改动涉及的测试类，不要跑全量测试套件**
   - 不管是写完新测试后自查，还是最终合并/发 PR 前的收尾验证，都用 `-Dtest=<改动涉及的测试类>` 精确限定范围。
   - 即使某个流程（如收尾合并的 skill）字面要求"跑完整测试套件"，也要先判断是否真的必要——多数历史项目的全量测试套件里混杂着大量跟本次改动无关、本身就有环境脆弱性的历史用例（如 PowerMock 静态 mock 冲突导致的 `NoClassDefFound`），跑全量只会引入无关噪音，还需要额外花时间去证明"这是历史遗留、不是本次引入的"。
   - **为什么**：曾经验证一个只改了 3 个文件的小改动时跑了全量测试（800+ 个测试，近 6 分钟），冒出 127 个无关 Error，还得切到基线分支对比才能证明跟本次改动无关——完全是不必要的开销。改动涉及的测试类全部通过，就足以证明这次改动没问题。
   - 只有当改动本身触及大范围公共代码、或用户明确要求"跑全量"时，才考虑全量跑。

### 常见 mock 坑速查表
| 坑 | 症状 | 解决方案 |
|---|---|---|
| Method 无法 mock | `Cannot mock/spy class java.lang.reflect.Method` | 用 `this.getClass().getMethod("name")` 取真实 Method |
| matcher 不配 | `Invalid use of argument matchers!` | 所有参数都用 matcher，或都用原值：`when(obj.method(eq(x), eq(y)))` |
| Throwable 未声明 | `未报告的异常错误java.lang.Throwable` | ProceedingJoinPoint 相关方法加 `throws Throwable` |
| static mock 泄露 | 前个测试的 mock 影响后个 | setUp() 中重新 `mockStatic` 或用 `@Before` 重新初始化 |

### 计时参考
- 同类 2 个测试类（30+ 个测试）：**10-12 分钟**（包括编译改错）
- 不要超过 5 分钟都在"侦查"代码结构