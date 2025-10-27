#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from web3 import Web3
import json
import os

# 加载ABI
with open('PositionManager.json', 'r') as f:
    position_manager_abi = json.load(f)

# BSC网络配置
BSC_RPC_URL = "https://bsc-dataseed.binance.org/"
POSITION_MANAGER_ADDRESS = "0x46A15B0b27311cedF172AB29E4f4766fbE7F4364"  # 请替换为实际的合约地址

# 连接到BSC网络
w3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
if not w3.is_connected():
    print("无法连接到BSC网络")
    exit(1)

# 创建合约实例
position_manager = w3.eth.contract(address=POSITION_MANAGER_ADDRESS, abi=position_manager_abi)

def query_position_info(token_id):
    """
    查询指定tokenId的池子信息
    """
    print(f"\n===== 查询TokenID: {token_id} 的信息 =====")
    
    try:
        # 查询流动性
        liquidity = position_manager.functions.getPositionLiquidity(token_id).call()
        print(f"流动性数量: {liquidity}")
        
        # 查询池子信息和代币信息
        pool_info = position_manager.functions.getPoolAndPositionInfo(token_id).call()
        
        # 解析poolKey
        pool_key = pool_info[0]
        currency0 = pool_key[0]
        currency1 = pool_key[1]
        fee = pool_key[2]
        tick_spacing = pool_key[3]
        hooks = pool_key[4]
        
        print("\n池子信息:")
        print(f"Currency0: {currency0}")
        print(f"Currency1: {currency1}")
        print(f"手续费率: {fee}")
        print(f"Tick间距: {tick_spacing}")
        print(f"Hooks合约: {hooks}")
        
        # 解析position info
        position_info = pool_info[1]
        print(f"\nPosition信息: {position_info}")
        
        return {
            "liquidity": liquidity,
            "currency0": currency0,
            "currency1": currency1,
            "fee": fee,
            "tick_spacing": tick_spacing,
            "hooks": hooks,
            "position_info": position_info
        }
    
    except Exception as e:
        print(f"查询出错: {str(e)}")
        return None

if __name__ == "__main__":
    # 用户输入tokenId
    while True:
        try:
            token_id_input = input("请输入要查询的TokenID (输入q退出): ")
            if token_id_input.lower() == 'q':
                break
                
            token_id = int(token_id_input)
            query_position_info(token_id)
            
        except ValueError:
            print("请输入有效的数字ID")
        except Exception as e:
            print(f"发生错误: {str(e)}")