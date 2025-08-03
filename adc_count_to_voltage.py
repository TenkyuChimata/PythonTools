def adc_count_to_voltage(adc_count: int, k: float = -5000.0, b: float = 26000.0) -> float:
    """
    将 ADC count 值转换为对应的电压值（考虑偏移量 b）
    :param adc_count: ADC 输出的原始计数值
    :param k: 斜率（默认 -5000）
    :param b: 偏移量（默认 26000）
    :return: 电压值（单位：伏特）
    """
    voltage = (b - adc_count) / -k
    return voltage

# 示例：
if __name__ == "__main__":
    count = int(input("请输入 ADC count 值喵："))
    voltage = adc_count_to_voltage(count)
    print(f"喵呜～ 对应的电压是 {voltage:.4f} V")
