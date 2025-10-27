#!/usr/bin/env python3
"""
BSC链上查询Uniswap V4 Position信息的脚本
通过tokenId查询池子信息，包括流动性和poolKey信息
"""

import json
from web3 import Web3

# BSC主网配置
BSC_RPC_URL = "https://bsc-dataseed1.binance.org/"
POSITION_MANAGER_ADDRESS = "0x7A4a5c919aE2541AeD11041A1AEeE68f1287f95b" # 请替换为实际的PositionManager合约地址

def load_abi():
    """加载PositionManager ABI"""
    try:
        with open('PositionManager.json', 'r') as f:
            abi = json.load(f)
        return abi
    except FileNotFoundError:
        print("错误: 找不到 PositionManager.json 文件")
        return None
    except json.JSONDecodeError:
        print("错误: PositionManager.json 文件格式错误")
        return None

def init_web3():
    """初始化Web3连接"""
    try:
        w3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
        if not w3.is_connected():
            print("错误: 无法连接到BSC网络")
            return None
        print(f"✅ 成功连接到BSC网络，当前区块: {w3.eth.block_number}")
        return w3
    except Exception as e:
        print(f"错误: 连接BSC网络失败 - {e}")
        return None

def get_position_info(w3, contract, token_id):
    """查询指定tokenId的位置信息"""
    try:
        print(f"\n🔍 查询 Token ID: {token_id}")
        
        # 1. 获取流动性
        print("📊 获取流动性信息...")
        liquidity = contract.functions.getPositionLiquidity(token_id).call()
        print(f"   流动性 (Liquidity): {liquidity}")
        
        # 2. 获取池子和位置信息
        print("🏊 获取池子和位置信息...")
        pool_info = contract.functions.getPoolAndPositionInfo(token_id).call()
        
        # 解析poolKey
        pool_key = pool_info[0]  # poolKey是第一个元素
        position_info = pool_info[1]  # positionInfo是第二个元素
        
        currency0 = pool_key[0]
        currency1 = pool_key[1]
        fee = pool_key[2]
        tick_spacing = pool_key[3]
        hooks = pool_key[4]
        
        print(f"   Currency0: {currency0}")
        print(f"   Currency1: {currency1}")
        print(f"   Fee: {fee}")
        print(f"   Tick Spacing: {tick_spacing}")
        print(f"   Hooks: {hooks}")
        print(f"   Position Info: {position_info}")
        
        # 3. 获取详细的位置信息
        print("📋 获取详细位置信息...")
        detailed_position_info = contract.functions.positionInfo(token_id).call()
        print(f"   详细位置信息: {detailed_position_info}")
        
        return {
            'token_id': token_id,
            'liquidity': liquidity,
            'pool_key': {
                'currency0': currency0,
                'currency1': currency1,
                'fee': fee,
                'tick_spacing': tick_spacing,
                'hooks': hooks
            },
            'position_info': position_info,
            'detailed_position_info': detailed_position_info
        }
        
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return None

def format_position_info(info):
    """格式化输出位置信息"""
    if not info:
        return
    
    print("\n" + "="*60)
    print(f"📍 Token ID: {info['token_id']}")
    print("="*60)
    print(f"💧 流动性: {info['liquidity']:,}")
    print(f"🪙 Currency0: {info['pool_key']['currency0']}")
    print(f"🪙 Currency1: {info['pool_key']['currency1']}")
    print(f"💰 手续费: {info['pool_key']['fee']} (0.{info['pool_key']['fee']/10000}%)")
    print(f"📏 Tick间距: {info['pool_key']['tick_spacing']}")
    print(f"🪝 Hooks合约: {info['pool_key']['hooks']}")
    print(f"ℹ️  位置信息: {info['position_info']}")
    print(f"📊 详细信息: {info['detailed_position_info']}")
    print("="*60)

def main():
    """主函数"""
    print("🚀 BSC链 Uniswap V4 Position 查询工具")
    print("="*50)
    
    # 加载ABI
    abi = load_abi()
    if not abi:
        return
    
    # 初始化Web3
    w3 = init_web3()
    if not w3:
        return
    
    
    
    # 创建合约实例
    try:
        contract = w3.eth.contract(
            address=Web3.to_checksum_address(POSITION_MANAGER_ADDRESS),
            abi=abi
        )
        print(f"✅ 合约实例创建成功: {POSITION_MANAGER_ADDRESS}")
    except Exception as e:
        print(f"❌ 创建合约实例失败: {e}")
        return
    
    # 交互式查询
    while True:
        try:
            print("\n" + "-"*50)
            token_id_input = input("请输入要查询的 Token ID (输入 'q' 退出): ").strip()
            
            if token_id_input.lower() == 'q':
                print("👋 再见!")
                break
            
            if not token_id_input.isdigit():
                print("❌ 请输入有效的数字")
                continue
            
            token_id = int(token_id_input)
            
            # 查询位置信息
            info = get_position_info(w3, contract, token_id)
            
            # 格式化输出
            format_position_info(info)
            
        except KeyboardInterrupt:
            print("\n👋 用户中断，再见!")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()