# -*- coding: utf-8 -*-

# 差分 ADC 增益计算（不含分压、电阻，单位 counts/V）
bits = 32          # ADC 总位数
vref = 2.5         # 参考电压
pga = 1            # ADC 增益

# 正满量程的最大数字码
max_code = 2**(bits - 1) - 1

# 每伏特对应多少 counts
counts_per_V = max_code / (vref / pga)

# 输出结果
print("Max code (positive full scale):", max_code)
print("Counts per V:", counts_per_V)
