from web3 import Web3
import json
import time 
# 连接 BSC 主网
w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org'))
if not w3.is_connected():
    raise Exception("Failed to connect to BSC node")

# 合约地址（校验和）
position_manager_address = Web3.to_checksum_address('0x7a4a5c919ae2541aed11041a1aeee68f1287f95b')

# 最小 ABI 作为回退，仅包含 modifyLiquidities / modifyLiquiditiesWithoutUnlock
MIN_POSITION_MANAGER_ABI = '[{"inputs":[{"internalType":"bytes","name":"unlockData","type":"bytes"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"modifyLiquidities","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes","name":"actions","type":"bytes"},{"internalType":"bytes[]","name":"params","type":"bytes[]"}],"name":"modifyLiquiditiesWithoutUnlock","outputs":[],"stateMutability":"payable","type":"function"}]'

# 加载 ABI（从 BscScan 下载，或使用简化版）
with open('PositionManager.json', 'r') as f:
    position_manager_abi = json.load(f)

# 如果 json 文件不包含 modifyLiquidities，则使用最小 ABI 回退
has_modify = any((item.get('type') == 'function' and item.get('name') == 'modifyLiquidities') for item in position_manager_abi)
if not has_modify:
    position_manager_abi = json.loads(MIN_POSITION_MANAGER_ABI)

# 创建合约实例
contract = w3.eth.contract(address=position_manager_address, abi=position_manager_abi)

# 假设参数（替换为你的实际值）
pool_key =  (
    Web3.to_checksum_address('0x55d398326f99059fF775485246999027B3197955'),
    Web3.to_checksum_address('0xfAB99fCF605fD8f4593EDb70A43bA56542777777'),
    9997,
    200,
    Web3.to_checksum_address('0x0000000000000000000000000000000000000000')
)  # PoolKey: (currency0, currency1, fee(uint24), tickSpacing(int24), hooks)

salt_hex = '000000000000000000000000000000000000000000000000000000000000DE44'  # 32字节盐值（十六进制）
if not salt_hex.startswith('0x'):
    salt_hex = '0x' + salt_hex
salt_bytes32 = Web3.to_bytes(hexstr=salt_hex)

liquidity = 0  # 要移除的流动性量；仅领取费用时为 0，如需撤出本金请设置为实际数值
recipient = Web3.to_checksum_address('0x0b5B86F9a031AD321f59D6B2615F46328f7d1987')  # 替换为你的钱包地址
zero_for_one = True  # 代币对方向（根据池排序）
deadline = int(time.time() + 1200)  # 当前时间 + 20 分钟

# -----------------------------
# 使用 PositionManager ABI 重构 unlock_data
# PositionManager.modifyLiquidities(bytes unlockData, uint256 deadline)
# unlockData = abi.encode(actions, params)
#   actions: bytes 序列（每个 action 一个字节/编号，具体编号由合约定义；这里使用 0x01=DecreaseLiquidity, 0x11=TakePair）
#   params: bytes[]，每个元素为对应 action 的参数 ABI 编码
# -----------------------------

# 1) 为 DecreaseLiquidity 编码参数: (uint256 tokenId, uint256 liquidity, uint128 amount0Min, uint128 amount1Min, bytes hookData)
#    注意：v4 PositionManager 的减少流动性参数是基于 position 的 tokenId；hookData 可为空字节
hook_data = b''
# 示例占位：请替换为你持有的仓位 NFT 的 tokenId
token_id = 59694
amount0_min = 0
amount1_min = 0
enc_decrease_params = w3.codec.encode_abi(
    ['uint256', 'uint128', 'uint128', 'uint128', 'bytes'],
    [token_id, liquidity, amount0_min, amount1_min, hook_data]
)

# 2) 为 TAKE_PAIR 编码参数: (Currency currency0, Currency currency1, address recipient)
#    Currency 在 ABI 中以 address 表示；若某一侧为原生币则使用 0 地址
enc_take_params = w3.codec.encode_abi(
    ['address', 'address', 'address'],
    [pool_key[0], pool_key[1], recipient]
)

# 3) 组装 actions 与 params
#    动作编号：DECREASE_LIQUIDITY=0x01，TAKE_PAIR=0x11
actions_bytes = bytes([0x01, 0x11])
params_bytes_array = [enc_decrease_params, enc_take_params]

# 4) 编码 unlockData: abi.encode(bytes, bytes[])
unlock_data_bytes = w3.codec.encode_abi(['bytes', 'bytes[]'], [actions_bytes, params_bytes_array])

# 5) 编码 modifyLiquidities 调用数据
modify_calldata = contract.encodeABI(fn_name='modifyLiquidities', args=[unlock_data_bytes, deadline])

# 输出十六进制（供链上或区块浏览器调试/调用）
print(f"unlockData (bytes hex): 0x{unlock_data_bytes.hex()}")
print(f"deadline (uint256): {deadline}")
print(f"modifyLiquidities calldata: {modify_calldata}")

# 可选：直接调用 modifyLiquiditiesWithoutUnlock（如果你不使用 lock/unlock 流程）
# 注意：modifyLiquiditiesWithoutUnlock 的签名是 (bytes actions, bytes[] params)
# calldata_without_unlock = contract.encodeABI(
#     fn_name='modifyLiquiditiesWithoutUnlock',
#     args=[actions_bytes, params_bytes_array]
# )
# print(f"modifyLiquiditiesWithoutUnlock calldata: {calldata_without_unlock}")