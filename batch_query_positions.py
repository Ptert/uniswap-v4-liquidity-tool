#!/usr/bin/env python3
"""
批量查询BSC链上Uniswap V4 Position信息
"""

import json
import csv
from web3 import Web3
from datetime import datetime

# BSC主网配置
BSC_RPC_URL = "https://bsc-dataseed1.binance.org/"
POSITION_MANAGER_ADDRESS = "0x..." # 请替换为实际的PositionManager合约地址

def load_abi():
    """加载PositionManager ABI"""
    with open('PositionManager.json', 'r') as f:
        return json.load(f)

def init_web3():
    """初始化Web3连接"""
    w3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
    if not w3.is_connected():
        raise Exception("无法连接到BSC网络")
    return w3

def query_single_position(contract, token_id):
    """查询单个位置信息"""
    try:
        # 获取流动性
        liquidity = contract.functions.getPositionLiquidity(token_id).call()
        
        # 获取池子和位置信息
        pool_info = contract.functions.getPoolAndPositionInfo(token_id).call()
        pool_key = pool_info[0]
        position_info = pool_info[1]
        
        return {
            'token_id': token_id,
            'liquidity': liquidity,
            'currency0': pool_key[0],
            'currency1': pool_key[1],
            'fee': pool_key[2],
            'tick_spacing': pool_key[3],
            'hooks': pool_key[4],
            'position_info': position_info,
            'status': 'success'
        }
    except Exception as e:
        return {
            'token_id': token_id,
            'error': str(e),
            'status': 'failed'
        }

def batch_query_positions(token_ids):
    """批量查询位置信息"""
    print(f"🚀 开始批量查询 {len(token_ids)} 个位置...")
    
    # 初始化
    abi = load_abi()
    w3 = init_web3()
    
    if POSITION_MANAGER_ADDRESS == "0x...":
        raise Exception("请设置正确的 POSITION_MANAGER_ADDRESS")
    
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(POSITION_MANAGER_ADDRESS),
        abi=abi
    )
    
    results = []
    successful = 0
    failed = 0
    
    for i, token_id in enumerate(token_ids, 1):
        print(f"📊 查询进度: {i}/{len(token_ids)} - Token ID: {token_id}")
        
        result = query_single_position(contract, token_id)
        results.append(result)
        
        if result['status'] == 'success':
            successful += 1
            print(f"   ✅ 成功 - 流动性: {result['liquidity']:,}")
        else:
            failed += 1
            print(f"   ❌ 失败 - {result['error']}")
    
    print(f"\n📈 查询完成! 成功: {successful}, 失败: {failed}")
    return results

def save_to_csv(results, filename=None):
    """保存结果到CSV文件"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"position_query_results_{timestamp}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'token_id', 'status', 'liquidity', 'currency0', 'currency1', 
            'fee', 'tick_spacing', 'hooks', 'position_info', 'error'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            # 填充缺失的字段
            row = {field: result.get(field, '') for field in fieldnames}
            writer.writerow(row)
    
    print(f"💾 结果已保存到: {filename}")
    return filename

def print_summary(results):
    """打印查询结果摘要"""
    successful_results = [r for r in results if r['status'] == 'success']
    
    if not successful_results:
        print("❌ 没有成功查询到任何位置信息")
        return
    
    print("\n" + "="*80)
    print("📊 查询结果摘要")
    print("="*80)
    
    # 统计不同的currency对
    currency_pairs = {}
    total_liquidity = 0
    
    for result in successful_results:
        pair = f"{result['currency0'][:6]}.../{result['currency1'][:6]}..."
        if pair not in currency_pairs:
            currency_pairs[pair] = {'count': 0, 'liquidity': 0}
        currency_pairs[pair]['count'] += 1
        currency_pairs[pair]['liquidity'] += result['liquidity']
        total_liquidity += result['liquidity']
    
    print(f"📈 总计查询成功: {len(successful_results)} 个位置")
    print(f"💧 总流动性: {total_liquidity:,}")
    print(f"🏊 涉及交易对: {len(currency_pairs)} 个")
    
    print("\n📋 交易对统计:")
    for pair, stats in currency_pairs.items():
        print(f"   {pair}: {stats['count']} 个位置, 流动性: {stats['liquidity']:,}")
    
    print("="*80)

def main():
    """主函数"""
    print("🚀 BSC链 Uniswap V4 Position 批量查询工具")
    print("="*60)
    
    # 示例用法
    print("\n使用方法:")
    print("1. 设置 POSITION_MANAGER_ADDRESS 为实际合约地址")
    print("2. 调用 batch_query_positions([token_id1, token_id2, ...]) 进行批量查询")
    print("3. 使用 save_to_csv() 保存结果")
    
    # 示例代码（注释掉，用户可以根据需要取消注释）
    """
    # 示例：查询多个token ID
    token_ids = [1, 2, 3, 4, 5]  # 替换为实际的token ID列表
    
    try:
        results = batch_query_positions(token_ids)
        save_to_csv(results)
        print_summary(results)
    except Exception as e:
        print(f"❌ 批量查询失败: {e}")
    """

if __name__ == "__main__":
    main()