# -*- coding: utf-8 -*-
import stun

def check_nat_type():
    # 猫娘用 STUN 服务来检测 NAT 类型喵～
    try:
        nat_type, external_ip, external_port = stun.get_ip_info(
            source_ip="0.0.0.0",
            source_port=54320,
            stun_host="stun.l.google.com",
            stun_port=19302
        )
        print("NAT 类型:", nat_type)
        print("外部 IP:", external_ip)
        print("外部端口:", external_port)
    except Exception as e:
        print("检查 NAT 类型时出错喵～", e)

if __name__ == "__main__":
    check_nat_type()
