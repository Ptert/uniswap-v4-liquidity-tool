#!/usr/bin/env python3
"""
BSC链上Uniswap V4 Position查询和unlockData生成工具
通过tokenId查询池子信息，并生成移除流动性所需的unlockData和deadline
"""

import json
import time
from datetime import datetime, timezone
from web3 import Web3
from eth_abi import encode

# BSC主网配置
BSC_RPC_URL = "https://bsc-dataseed1.binance.org/"
POSITION_MANAGER_ADDRESS = "0x7A4a5c919aE2541AeD11041A1AEeE68f1287f95b"  # PositionManager合约地址

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
            'position_info': position_info
        }
        
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return None

def encode_modify_liquidities_unlock_data(
    token_id: int,
    currency0: str,
    currency1: str,
    recipient: str,
    liquidity: int = 0,
    amount0_min: int = 0,
    amount1_min: int = 0,
    hook_data: bytes = b'',
) -> str:
    """按 v4 PositionManager 的参数约定，编码 unlockData = abi.encode(actions(bytes), params(bytes[]))。
    动作序列为 [0x01 (DECREASE_LIQUIDITY), 0x11 (TAKE_PAIR)]。
    返回 0x 前缀的十六进制字符串。
    """
    # 编码 DECREASE_LIQUIDITY 参数 (uint256 tokenId, uint128 liquidity, uint128 amount0Min, uint128 amount1Min, bytes hookData)
    dec_params = encode(
        ['uint256', 'uint128', 'uint128', 'uint128', 'bytes'],
        [int(token_id), int(liquidity), int(amount0_min), int(amount0_min), hook_data]
    )

    # 编码 TAKE_PAIR 参数 (address currency0, address currency1, address recipient)
    take_params = encode(
        ['address', 'address', 'address'],
        [Web3.to_checksum_address(currency0), Web3.to_checksum_address(currency1), Web3.to_checksum_address(recipient)]
    )

    actions_bytes = bytes([0x01, 0x11])
    unlock_data_bytes = encode(['bytes', 'bytes[]'], [actions_bytes, [dec_params, take_params]])
    return '0x' + unlock_data_bytes.hex()

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
    print("="*60)

def generate_unlock_data(position_info, recipient):
    """根据位置信息和接收地址生成unlockData和deadline"""
    token_id = position_info['token_id']
    liquidity = position_info['liquidity']
    currency0 = position_info['pool_key']['currency0']
    currency1 = position_info['pool_key']['currency1']
    
    # 为避免滑点，可以设置最小值，这里默认为0
    amount0_min = 0
    amount1_min = 0
    hook_data = b''
    
    # 生成unlockData
    unlock_hex = encode_modify_liquidities_unlock_data(
        token_id, currency0, currency1, recipient,
        liquidity, amount0_min, amount1_min, hook_data
    )
    
    # 生成deadline (当前时间 + 20分钟)
    deadline_int = int(time.time() + 1200)
    deadline_local = datetime.fromtimestamp(deadline_int, tz=timezone.utc).astimezone().isoformat()
    
    return {
        'unlock_data': unlock_hex,
        'deadline': deadline_int,
        'deadline_local': deadline_local
    }

def main():
    """主函数"""
    print("🚀 BSC链 Uniswap V4 Position 查询和unlockData生成工具")
    print("="*60)
    
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
    
    # 交互式查询和生成
    while True:
        try:
            print("\n" + "-"*60)
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
            if not info:
                continue
            
            # 格式化输出位置信息
            format_position_info(info)
            
            # 询问是否生成unlockData
            generate = input("\n是否生成移除流动性的unlockData? (y/n): ").strip().lower()
            if generate != 'y':
                continue
            
            # 输入接收地址
            recipient = input("请输入接收地址 (接收移除流动性后的代币): ").strip()
            if not Web3.is_address(recipient):
                print("❌ 无效的地址格式")
                continue
            
            # 确保地址格式正确
            recipient = Web3.to_checksum_address(recipient)
            
            # 生成unlockData和deadline
            unlock_result = generate_unlock_data(info, recipient)
            
            print("\n" + "="*60)
            print("🔑 生成的unlockData和deadline:")
            print("="*60)
            print(f"unlockData (bytes hex): {unlock_result['unlock_data']}")
            print(f"deadline (uint256): {unlock_result['deadline']}")
            print(f"deadline本地时间: {unlock_result['deadline_local']}")
            print("="*60)
            
        except KeyboardInterrupt:
            print("\n👋 用户中断，再见!")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()